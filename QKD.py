from qiskit import QuantumCircuit, Aer, execute
from numpy.random import randint
import os

def e91_prepare_qubits(num_qubits):
    qubits = []
    for _ in range(num_qubits):
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])
        qubits.append(qc)
    return qubits

def e91_send_qubits_to_bob(qubits):
    received_qubits = []
    for qc in qubits:
        backend = Aer.get_backend('qasm_simulator')
        job = execute(qc, backend, shots=1)
        result = job.result()
        counts = result.get_counts(qc)
        received_qubits.append(counts)
    return received_qubits

def e91_measure_qubits(received_qubits):
    measurements = []
    for counts in received_qubits:
        if '00' in counts:
            measurements.append(0)
        elif '11' in counts:
            measurements.append(1)
    return measurements

def e91_compare_bases(bases_a, bases_b):
    matching_bases = []
    for i in range(len(bases_a)):
        if bases_a[i] == bases_b[i]:
            matching_bases.append(i)
    return matching_bases

def e91_extract_key_bits(qubits, matching_bases):
    key_bits = ''
    for i in matching_bases:
        qc = qubits[i]
        backend = Aer.get_backend('qasm_simulator')
        job = execute(qc, backend, shots=1)
        result = job.result()
        counts = result.get_counts(qc)
        key_bits += list(counts.keys())[0][0]
    return key_bits

def e91_secure_data_transmission(num_qubits):
    a_qubits = e91_prepare_qubits(num_qubits)
    r_received_qubits = e91_send_qubits_to_bob(a_qubits)
    b_measurements = e91_measure_qubits(r_received_qubits)
    a_bases = randint(2, size=num_qubits)
    matching_bases = e91_compare_bases(a_bases, b_measurements)
    key_bits = e91_extract_key_bits(a_qubits, matching_bases)
    return key_bits

def bell_test(qubits):
    bell_circuit = QuantumCircuit(2, 2)
    bell_circuit.h(0)
    bell_circuit.cx(0, 1)
    bell_circuit.measure([0, 1], [0, 1])

    backend = Aer.get_backend('qasm_simulator')
    job = execute(qubits + [bell_circuit], backend, shots=1)
    result = job.result()
    counts = result.get_counts(bell_circuit)
    return counts

def detect_bells_inequality_violation(num_qubits):
    a_qubits = e91_prepare_qubits(num_qubits)
    b_results = bell_test(a_qubits)
    if '00' in b_results or '11' in b_results:
        return False  
    else:
        return True  

def get_encryption_key():
    key_file = "encryption_key.txt"
    if os.path.exists(key_file):
        with open(key_file, "r") as f:
            encryption_key = f.read().strip()
    else:
        encryption_key = e91_secure_data_transmission(100)
        with open(key_file, "w") as f:
            f.write(encryption_key)
    return encryption_key

def encrypt_data(data, key):
    encrypted_data = ''
    for i in range(len(data)):
        char_code = ord(data[i])
        encrypted_char_code = char_code ^ ord(key[i % len(key)])
        encrypted_data += chr(encrypted_char_code)
    return encrypted_data

def decrypt_data(encrypted_data, key):
    decrypted_data = ''
    for i in range(len(encrypted_data)):
        encrypted_char_code = ord(encrypted_data[i])
        decrypted_char_code = encrypted_char_code ^ ord(key[i % len(key)])
        decrypted_data += chr(decrypted_char_code)
    return decrypted_data

encryption_key = get_encryption_key()

billing_data = "Shyaam2445"
encrypted_billing_data = encrypt_data(billing_data, encryption_key)
print("Encrypted billing data:", encrypted_billing_data)

decrypted_billing_data = decrypt_data(encrypted_billing_data, encryption_key)
print("Decrypted billing data:", decrypted_billing_data)

bell_inequality_violated = detect_bells_inequality_violation(100)
if bell_inequality_violated:
    print("Bell's inequality violated. Potential eavesdropping detected.")
else:
    print("Bell's inequality not violated.")