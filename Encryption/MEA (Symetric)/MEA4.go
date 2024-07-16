package main

import (
	"fmt"
	"os"
	"math/rand"
	"time"
)

func plaintext_to_bytes(input string) []byte {
	return []byte(input)
}

func bytes_to_plaintext(input []byte) string {
	return string(input)
}

func key_expansion(key []byte) []byte {
	if len(key) != 64 {
		panic("Input key must be 64 bytes long")
	}

	subkey := make([]byte, 64)

	for i := 0; i < 64; i++ {
		subkey[i] = (key[i] ^ byte(i))<<1 | (key[i] ^ byte(i))>>7
	}

	for i := 0; i < 64; i += 2 {
		subkey[i], subkey[i+1] = subkey[i+1], subkey[i]
	}

	return subkey
}
func random_bytes(amount int) []byte {
	file, err := os.Open("/dev/urandom")
	if err != nil {
		fmt.Println(err)
	}

	randomBytes := make([]byte, amount)

	_, err = file.Read(randomBytes)
	if err != nil {
		fmt.Println(err)
	}
	file.Close()

	return randomBytes
}

func shuffle(data []byte, key []byte) []byte {
	seed := int64(0)
	for _, b := range key {
		seed = seed*31 + int64(b)
	}
	rnd := rand.New(rand.NewSource(seed))
	shuffled := make([]byte, len(data))
	perm := rnd.Perm(len(data))
	for i, v := range perm {
		shuffled[v] = data[i]
	}
	return shuffled
}

func unshuffle(data []byte, key []byte) []byte {
	seed := int64(0)
	for _, b := range key {
		seed = seed*31 + int64(b)
	}
	rnd := rand.New(rand.NewSource(seed))
	unshuffled := make([]byte, len(data))
	perm := rnd.Perm(len(data))
	for i, v := range perm {
		unshuffled[i] = data[v]
	}
	return unshuffled
}

func XOR(input []byte, key []byte) []byte {
	result := make([]byte, len(input))

	for i := 0; i < len(input); i++ {
		result[i] = input[i] ^ key[i % len(key)]
	}

	return result
}

func encrypt(input string, key []byte, rounds int) []byte {
	plaintextByteArray := plaintext_to_bytes(input)
	iv := random_bytes(16)
	combined := append(plaintextByteArray, iv...)

	output := combined

	for i := 0; i < rounds; i++ {
		sk := key_expansion(key)
	
		shuffle1 := shuffle(output, sk)

		xored := XOR(shuffle1, sk)

		output = shuffle(xored, sk)
	}

	return output
}

func decrypt(input []byte, key []byte, rounds int) []byte {
	output := input

	for i := 0; i < rounds; i++ {
		sk := key_expansion(key)

		unshuffle2 := unshuffle(output, sk)
	
		xored := XOR(unshuffle2, sk)

		output = unshuffle(xored, sk)
	}

	removed_iv := output[:len(output)-16]

	return removed_iv
}

func main() {
	plaintext := ("Hello bro, are you cool?")

	key := random_bytes(64) // 512 bits

	start_enc := time.Now()
	encrypted := encrypt(plaintext, key, 2)
	duration_enc := time.Since(start_enc)

	start_dec := time.Now()
	decrypted := decrypt(encrypted, key, 2)
	duration_dec := time.Since(start_dec)

	fmt.Println("Encrypted: ",bytes_to_plaintext(encrypted))
	fmt.Println("Decrypted: ",bytes_to_plaintext(decrypted))
	fmt.Println("Encryption took:", duration_enc)
	fmt.Println("Decryption took:", duration_dec)
}

//under dev