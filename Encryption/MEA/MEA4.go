/*
Encryption Algorithm Version 4
Copyright (C) 2024  meduggit

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/


package main

import (
	"fmt"
	"os"
	"bytes"
	"log"
)


func pad(data []byte, blockSize int) [][]byte {
	paddingSize := blockSize - (len(data) % blockSize)
	paddedData := append(data, bytes.Repeat([]byte{byte(paddingSize)}, paddingSize)...)

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

func unpad(data []byte) []byte {
	paddingSize := data[len(data)-1]
	return data[:len(data)-int(paddingSize)]
}

func keyExpansion(key []byte, n int, lenght int) []byte {
    subkey := make([]byte, lenght)

    for i := 0; i < lenght; i++ {
        subkey[i] = (key[i] ^ byte(i) ^ byte(n))<<1 | (key[i] ^ byte(i) ^ byte(n))>>7
    }

    for i := 0; i < lenght; i += 2 {
        if (i/2)%2 == n%2 {
            subkey[i], subkey[i+1] = subkey[i+1], subkey[i]
        }
    }

    return subkey
}

func randomBytes(amount int) []byte {
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

func applySBox(originalBytes []byte, sbox []byte) []byte {
	result := make([]byte, len(originalBytes))

	for i, b := range originalBytes {
		result[i] = sbox[b]
	}

	return result
}

func createSeed(key []byte) int64 {
	seed := int64(0x1F3A5B9D)
	for _, b := range key {
		seed = (seed * 31) ^ int64(b)
	}
	return seed & ((1 << 48) - 1)
}

func createPermutation(key []byte, length int) []int {
	seed := createSeed(key)
	permutation := make([]int, length)
	for i := range permutation {
		permutation[i] = i
	}

	for i := length - 1; i > 0; i-- {
		seed = (seed*0x5DEECE66D + 0xB) & ((1 << 48) - 1)
		j := int(seed % int64(i+1))
		permutation[i], permutation[j] = permutation[j], permutation[i]
	}

	return permutation
}

func shuffle(input []byte, key []byte) []byte {
	permutation := createPermutation(key, len(input))
	output := make([]byte, len(input))

	for i, p := range permutation {
		output[p] = input[i]
	}

	return output
}

func unshuffle(input []byte, key []byte) []byte {
	permutation := createPermutation(key, len(input))
	output := make([]byte, len(input))

	for i, p := range permutation {
		output[i] = input[p]
	}

	return output
}

func splitByteSlices(input []byte, sliceSize int) [][]byte {
    if len(input)%sliceSize != 0 {
        log.Fatalf("Input length must be divisible by %d", sliceSize)
    }

    numSlices := len(input) / sliceSize
    result := make([][]byte, numSlices)

    for i := 0; i < numSlices; i++ {
        start := i * sliceSize
        end := start + sliceSize
        result[i] = input[start:end]
    }

    return result
}

func blockCipherEncrypt(input []byte, key []byte) []byte {
	var encryptedOutput []byte
	
	rk := keyExpansion(key, 0, len(key))

	shuffledInput := shuffle(input, rk)

	var xorShuffled []byte

	for b := 0; b < len(shuffledInput); b++ {
		xorBytes := shuffledInput[b] ^ rk[b]
		xorShuffled = append(xorShuffled, xorBytes) 
	}

	sboxXor := applySBox(xorShuffled, SBox)

	encryptedOutput = sboxXor

	return encryptedOutput
}

func blockCipherDecrypt(encryptedInput []byte, key []byte) []byte {
    var decryptedOutput []byte

    rk := keyExpansion(key, 0, len(key))

    sboxInverse := applySBox(encryptedInput, InvSBox)

    var xorBytes []byte

    for b := 0; b < len(sboxInverse); b++ {
        xorBytes = append(xorBytes, sboxInverse[b] ^ rk[b])
    }

    shuffledOutput := unshuffle(xorBytes, rk)

    decryptedOutput = shuffledOutput

    return decryptedOutput
}

func processEncryption(input []byte, key []byte, iv []byte , blockSize int) []byte {
	paddedData := pad(input, blockSize)

	var cipherText []byte

	prevBlock := iv

	for _, block := range paddedData {
		xoredBlock := make([]byte, blockSize)
		for b := 0; b < blockSize; b++ {
			xoredBlock[b] = block[b] ^ prevBlock[b]
		}

		encryptedBlock := blockCipherEncrypt(xoredBlock, key)
		cipherText = append(cipherText, encryptedBlock...)

		prevBlock = encryptedBlock
	}

	return cipherText
}

func processDecryption(input []byte, key []byte, iv []byte, blockSize int) []byte {
	blocks := splitByteSlices(input, blockSize)

	var plaintext []byte

	previousBlock := iv

	for _, block := range blocks {
		decryptedBlock := blockCipherDecrypt(block, key)

		plainBlock := make([]byte, blockSize)
		for i := 0; i < blockSize; i++ {
			plainBlock[i] = decryptedBlock[i] ^ previousBlock[i]
		}

		plaintext = append(plaintext, plainBlock...)

		previousBlock = block
	}

	return unpad(plaintext)
}

func main() {
	originalData := []byte("test msg")
	key := randomBytes(64)
	iv := randomBytes(64)

	stateSize := 64

	encrypted := processEncryption(originalData, key, iv, stateSize)

	fmt.Println("encrypted:", encrypted)

	decrypted := processDecryption(encrypted, key, iv, stateSize)

	fmt.Println("decrypted:", string(decrypted))
}	