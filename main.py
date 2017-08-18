rotor_I = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "R"]
rotor_II = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "AJDKSIRUXBLHWTMCQGZNPYFVOE", "F"]
rotor_III = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "BDFHJLCPRTXVZNYEIWGAKMUSQO", "W"]
rotor_IV = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "ESOVPZJAYQUIRHXLNFTGKDCMWB", "K"]
rotor_V = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "VZBRGITYUPSDNHLXAWMJQOFECK", "A"]
reflector_B = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "YRUHQSLDPXNGOKMIEBFZCWVJAT"]
reflector_C = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "FVPJIAOYEDRZXWGCTKUQSBNMHL"]
static_rotor = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
rotors = [rotor_I, rotor_II, rotor_III]

def set_rotor(char, rotor):
    index = rotor[0].index(char)
    for i in range(index):
        rotor[0] += rotor[0][i]
        rotor[1] += rotor[1][i]
    rotor[0] = rotor[0][index:]
    rotor[1] = rotor[1][index:]


def shift_rotor(rotor):
    rotor[0] += rotor[0][0]
    rotor[1] += rotor[1][0]
    rotor[0] = rotor[0][1:]
    rotor[1] = rotor[1][1:]

def main():
    print("Opening key file, loading settings...")
    settings = []
    rotors_ordered = []
    with open("key.txt", 'r') as file:
        for lines in file:
            if lines[0] == '#':
                continue
            else:
                settings.append(lines[:-1])

    for rot in settings[0]:
        if int(rot) > 5:
            print("Key error. One of the rotor numbers are wrong. Program will exit")
            return
    if settings[2] != 'B' and settings[2] != 'C':
        print("Key error. Reflector type is wrong. Program will exit")
        return

    rotors_ordered.append(rotors[int(settings[0][2]) - 1])
    rotors_ordered.append(rotors[int(settings[0][1]) - 1])
    rotors_ordered.append(rotors[int(settings[0][0]) - 1])

    set_rotor(settings[1][0], rotors_ordered[2])
    set_rotor(settings[1][1], rotors_ordered[1])
    set_rotor(settings[1][2], rotors_ordered[0])
    if settings[2] == 'B':
        reflector = reflector_B
    else:
        reflector = reflector_C
    settings[3] = settings[3].split(',')
    plugboard_alphabet = ""

    for i in range(len(settings[3])):
        plugboard_alphabet += settings[3][i][0]
    for i in range(len(settings[3])):
        plugboard_alphabet += settings[3][i][1]

    plugboard = [plugboard_alphabet, plugboard_alphabet[::-1]]
    plain_text = input("Type text to encrypt/decrypt: ")
    plain_text = plain_text.upper()
    output_text = ""
    flag = False
    for c in plain_text:
        if 65 > ord(c) < 90:
            output_text += c
        else:
            shift_rotor(rotors_ordered[0])
            if rotors_ordered[0][0][0] == rotors_ordered[0][2]:
                shift_rotor(rotors_ordered[1])
                flag = False
            if rotors_ordered[1][0][0] == rotors_ordered[1][2] and flag is not True:
                shift_rotor(rotors_ordered[2])
                flag = True
            if c in plugboard[0]:
                c = plugboard[1][plugboard[0].index(c)]
            ind = static_rotor[0].index(c)

            crypted_char = rotors_ordered[0][1][ind]
            ind = rotors_ordered[0][0].index(crypted_char)
            crypted_char = rotors_ordered[1][1][ind]
            ind = rotors_ordered[1][0].index(crypted_char)

            crypted_char = rotors_ordered[2][1][ind]
            ind = rotors_ordered[2][0].index(crypted_char)

            crypted_char = reflector[1][ind]
            ind = reflector[0].index(crypted_char)

            crypted_char = rotors_ordered[2][0][ind]
            ind = rotors_ordered[2][1].index(crypted_char)

            crypted_char = rotors_ordered[1][0][ind]
            ind = rotors_ordered[1][1].index(crypted_char)

            crypted_char = rotors_ordered[0][0][ind]
            ind = rotors_ordered[0][1].index(crypted_char)

            crypted_char = static_rotor[0][ind]
            if crypted_char in plugboard[0]:
                crypted_char = plugboard[1][plugboard[0].index(crypted_char)]
            output_text += crypted_char

    print(output_text)

if __name__ == "__main__":
    main()