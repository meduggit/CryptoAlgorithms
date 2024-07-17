// This file is licensed under the GNU General Public License v3.0.
// See LICENSE.md file for details.
//
// Copyright (c) meduggit 2024



package main

import (
	"bytes"
	"fmt"
	"math/rand"
	"os"
	"time"
)

// Pad adds PKCS#7 padding and splits data into 32-byte blocks
func Pad(data []byte, blockSize int) [][]byte {
	// Calculate how many padding bytes are needed
	paddingSize := blockSize - (len(data) % blockSize)
	paddedData := append(data, bytes.Repeat([]byte{byte(paddingSize)}, paddingSize)...)

	// Split into blocks
	var blocks [][]byte
	for i := 0; i < len(paddedData); i += blockSize {
		end := i + blockSize
		if end > len(paddedData) {
			end = len(paddedData)
		}
		blocks = append(blocks, paddedData[i:end])
	}

	return blocks
}

// Unpad removes PKCS#7 padding from the last block of data
func Unpad(data []byte) []byte {
	paddingSize := data[len(data)-1]
	return data[:len(data)-int(paddingSize)]
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

//////////////////////////////////////////
//				SHUFFLING				//
//////////////////////////////////////////

func createSeed(key []byte) int64 {
    seed := int64(0)
    for _, b := range key {
        seed += int64(b) // Sum bytes for seed
    }
    return seed
}

// Shuffle shuffles the input slice using the given key
func Shuffle(input []byte, key []byte) []byte {
    seed := createSeed(key)
    rng := rand.New(rand.NewSource(seed))

    output := make([]byte, len(input))
    copy(output, input)

    for i := len(output) - 1; i > 0; i-- {
        j := rng.Intn(i + 1)
        output[i], output[j] = output[j], output[i]
    }
    return output
}

// Unshuffle reverses the shuffle using the given key
func Unshuffle(input []byte, key []byte) []byte {
    seed := createSeed(key)
    rng := rand.New(rand.NewSource(seed))

    output := make([]byte, len(input))
    copy(output, input)

    indices := make([]int, len(output))
    for i := range indices {
        indices[i] = i
    }

    for i := len(indices) - 1; i > 0; i-- {
        j := rng.Intn(i + 1)
        indices[i], indices[j] = indices[j], indices[i]
    }

    original := make([]byte, len(input))
    for i, index := range indices {
        original[index] = output[i]
    }

    return original
}

//////////////////////////////////////////
//				CODE CNT.				//
//////////////////////////////////////////

func RotateLeft(slice []byte, n int) []byte {
	length := len(slice)
	if length == 0 || n%length == 0 {
		return slice
	}
	n = n % length
	return append(slice[n:], slice[:n]...)
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

func encrypt(plaintextBytes []byte, keyBytes []byte) []byte {
	var outputEncrypted []byte

	IV := random_bytes(32)

	plaintextBytes = append(plaintextBytes, IV...)

	var shuffledBytes []byte

	for SA := 0; SA < 2; SA++ {
		shuffledBytes = Shuffle(plaintextBytes, keyBytes)
		plaintextBytes = shuffledBytes
	}

	paddedBytes := Pad(shuffledBytes, 32)

	for block := 0; block < len(paddedBytes); block++ {
		for b := 0; b < 32; b++ {
			encryptedBytes := paddedBytes[block][b] ^ keyBytes[b]
			outputEncrypted = append(outputEncrypted, encryptedBytes)
		}
	}

	outputEncrypted = Shuffle(outputEncrypted, keyBytes)

	return outputEncrypted
}

func decrypt(encryptedBytes []byte, keyBytes []byte) []byte {
	var decryptedOutput []byte

	encryptedBytes = Unshuffle(encryptedBytes, keyBytes)

	// XOR to decrypt
	for b := 0; b < len(encryptedBytes); b++ {
		decryptedBytes := encryptedBytes[b] ^ keyBytes[b%32] // Use modulo to cycle through keyBytes
		decryptedOutput = append(decryptedOutput, decryptedBytes)
	}

	// Split decryptedOutput into 32-byte slices
	var blocks [][]byte
	for i := 0; i < len(decryptedOutput); i += 32 {
		end := i + 32
		if end > len(decryptedOutput) {
			end = len(decryptedOutput)
		}
		blocks = append(blocks, decryptedOutput[i:end])
	}

	if len(blocks) > 0 {
		blocks[len(blocks)-1] = Unpad(blocks[len(blocks)-1])
	}

	var byteSliceBlocks []byte

	for block := 0; block < len(blocks); block++ {
		byteSliceBlocks = append(byteSliceBlocks, blocks[block]...)
	}

	for SA := 0; SA < 2; SA++ {
		unshuffledBytes := Unshuffle(byteSliceBlocks, keyBytes)
		byteSliceBlocks = unshuffledBytes
	}

	return byteSliceBlocks[:len(byteSliceBlocks)-32]
}

func main() {
	originalData := []byte("Hello, world! Have you heard the news? Trump was a victim of an attempted assassination!")
	key := []byte{201, 111, 197, 60, 192, 18, 235, 17, 9, 153, 244, 60, 58, 192, 211, 235, 60, 117, 172, 9, 38, 66, 176, 15, 8, 144, 98, 127, 201, 95, 148, 96}

	start_enc := time.Now()
	encrypted := encrypt(originalData, key)
	fmt.Println("Encrypted:", encrypted)
	duration_enc := time.Since(start_enc)

	start_dec := time.Now()
	decrypted := string(decrypt(encrypted, key))
	fmt.Println("Decrypted:", decrypted)
	duration_dec := time.Since(start_dec)
	fmt.Println("Encryption took:", duration_enc)
	fmt.Println("Decryption took:", duration_dec)

}