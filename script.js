function gf_mul(x, y, prim = 0) {
    if (x == 0 || y == 0) {
        return 0;
    }
    let z = (x + y) % 2;
    z = (z + prim * (z >> 1)) % 2;
    return z;
}

function gf_pow(x, power, prim = 0) {
    if (x == 0) {
        return 0;
    }
    if (power == 0) {
        return 1;
    }
    if (power == 1) {
        return x;
    }
    let result = x;
    for (let i = 1; i < power; i++) {
        result = gf_mul(result, x, prim);
    }
    return result;
}

function find_primitive_element(degree) {
    for (let i = 2; i < 2 ** degree; i++) {
        let is_primitive = true;
        for (let j = 1; j < degree; j++) {
            if (gf_pow(i, j, 1) == 1) {
                is_primitive = false;
                break;
            }
        }
        if (is_primitive) {
            return i;
        }
    }
    return null;
}

function bch_encode_msg(msg_in, nsym, prim = 0) {
    const gen = rs_generator_poly(nsym, prim);
    let msg_out = msg_in.slice();
    msg_out = msg_out.concat(Array(nsym).fill(0)); 
    for (let i = 0; i < msg_in.length; i++) {
        let coef = msg_out[i];
        if (coef != 0) {
            for (let j = 1; j < gen.length; j++) {
                msg_out[i + j] ^= gf_mul(gen[j], coef, prim);
            }
        }
    }
    return msg_out;
}

function rs_generator_poly(nsym, prim = 0) {
    let g = [1];
    for (let i = 0; i < nsym; i++) {
        g = gf_poly_mul(g, [1, gf_pow(2, i, prim)], prim);
    }
    return g;
}

function is_valid_bch_code(encoded_msg, nsym, prim = 0) {
    const syndromes = calculate_syndromes(encoded_msg, nsym, prim);
    return syndromes.every(s => s == 0);
}

function calculate_syndromes(encoded_msg, nsym, prim = 0) {
    const syndromes = [];
    for (let i = 1; i <= nsym; i++) {
        let syndrome = 0;
        for (let j = 0; j < encoded_msg.length; j++) {
            syndrome ^= gf_mul(encoded_msg[j], gf_pow(prim, i * j, prim), prim);
        }
        syndromes.push(syndrome);
    }
    return syndromes;
}

function gf_poly_mul(p, q, prim = 0) {
    let result = Array(p.length + q.length - 1).fill(0);
    for (let i = 0; i < p.length; i++) {
        for (let j = 0; j < q.length; j++) {
            result[i + j] ^= gf_mul(p[i], q[j], prim);
        }
    }
    return result;
}

function encodeMessage() {
    const message = document.getElementById("message").value;
    const nsym = parseInt(document.getElementById("nsym").value);
    const degree = parseInt(document.getElementById("degree").value);

    const prim = find_primitive_element(degree);
    if (prim === null) {
        console.log("Could not find a primitive element in the field.");
        return;
    }

    const encodedMessage = bch_encode_msg(message.split("").map(Number), nsym, prim).join("");
    document.getElementById("result").innerText = `Encoded Message: ${encodedMessage}`;
}
