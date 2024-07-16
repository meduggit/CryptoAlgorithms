package main

import (
    "fmt"
    "time"
)

const version string = "MHF6"

func PadAndDivide(input []byte) [][]byte {
    // If the input is empty, start with just 0x01 and pad
    if len(input) == 0 {
        input = []byte{0x01}
    }

    // Calculate the original length
    originalLength := len(input)

    // Calculate padding length
    paddingLength := 64 - (originalLength % 64)
    if paddingLength == 64 {
        paddingLength = 0 // No padding needed if already a multiple of 64
    }

    // Create a padded slice of appropriate length
    padded := make([]byte, originalLength+paddingLength+1)
    copy(padded, input)

    // Append 0x01
    padded[originalLength] = 0x01

    // Fill remaining bytes with 0x00
    for i := originalLength + 1; i < len(padded); i++ {
        padded[i] = 0x00
    }

    // Calculate number of 64-byte blocks
    blockCount := len(padded) / 64
    result := make([][]byte, blockCount)

    // Divide into 64-byte slices
    for i := 0; i < blockCount; i++ {
        result[i] = padded[i*64 : (i+1)*64]
    }

    return result
}

func RotateLeft(slice []byte, n int) []byte {
	length := len(slice)
	if length == 0 || n%length == 0 {
		return slice
	}
	n = n % length
	return append(slice[n:], slice[:n]...)
}

func shuffle(data []byte, key []byte) []byte {
	if len(data) == 0 {
		return nil
	}

	var seed int64 = 0
	for _, b := range data {
		seed = seed*31 + int64(b)
	}

	shuffled := make([]byte, len(data))
	for i, b := range data {
		idx := (seed + int64(i) + int64(key[i%len(key)])) % int64(len(data))
		if idx < 0 {
			idx += int64(len(data))
		}
		shuffled[idx] = b
	}

	return shuffled
}

func mixing(input []byte, rotationAmount int, rounds int) []byte {
	for r := 0; r < rounds; r++ {
		rotatedL := RotateLeft(input, rotationAmount)
		shuffled := shuffle(input, input)

		var temp []byte
		for i := 0; i < len(input); i++ {
			temp = append(temp, rotatedL[i]^shuffled[i])
		}

		input = temp
	}

	return input
}

func processing(input []byte, mode string) []byte {
	inputBlocks := PadAndDivide(input)

	sum := 0
	for _, value := range input {
		sum += int(value)
	}

	if mode == "FAST" {
		sum = (sum % 370)
	} else if mode == "PSWD" {
		sum = sum * 32
	}

	S1 := []byte{222, 81, 171, 23, 90, 148, 226, 99, 244, 125, 19, 243, 133, 18, 42, 159, 6, 246, 130, 48, 216, 35, 8, 166, 119, 44, 198, 248, 135, 138, 200, 96, 243, 182, 221, 231, 114, 37, 21, 15, 28, 228, 175, 144, 31, 114, 50, 144, 95, 248, 3, 180, 30, 181, 113, 203, 57, 167, 66, 55, 118, 91, 168, 175}
	S2 := []byte{96, 104, 55, 23, 78, 232, 169, 176, 32, 184, 70, 147, 224, 172, 80, 196, 148, 24, 18, 152, 57, 123, 22, 226, 142, 76, 242, 6, 173, 215, 75, 29, 59, 43, 193, 204, 211, 17, 224, 115, 223, 122, 249, 117, 181, 227, 14, 51, 117, 85, 101, 145, 78, 151, 113, 130, 115, 89, 95, 31, 128, 11, 4, 205}
	
	S1Mixed := mixing(S1, sum, sum)
	S2SHuffled := shuffle(S2, S1)

	var output []byte
	
	for block := 0; block < len(inputBlocks); block++ {
		var outputBlock []byte
		for b := 0; b < 64; b++ {
			outputByte := ((inputBlocks[block][b] ^ S1[b]) ^ S2SHuffled[b] ^ S1Mixed[b]) ^ S2SHuffled[b]
			outputBlock = append(outputBlock, outputByte)
		}
		output = shuffle(outputBlock, input)
	}

	return output	
}

func main() {
    MODE := "FAST" // FAST or PSWD
	
    input := []byte("cool test") // Example input
    startDec := time.Now()
    output := processing(input, MODE)
    durationDec := time.Since(startDec)
    fmt.Println("Output: ", output)
    fmt.Println("Operation took:", durationDec)
    fmt.Println(len(output))
}

//under dev