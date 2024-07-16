package main

import (
    "fmt"
    "time"
)

const version string = "MHF6"

func PadAndDivide(input []byte) [][]byte {
    var result [][]byte
    chunkSize := 32

    for i := 0; i < len(input); i += chunkSize {
        end := i + chunkSize
        if end > len(input) {
            end = len(input)
        }
        chunk := make([]byte, chunkSize)
        copy(chunk, input[i:end])

        if end-i < chunkSize {
            chunk[end-i] = 0x01
            for j := end - i + 1; j < chunkSize; j++ {
                chunk[j] = 0x00
            }
        }

        result = append(result, chunk)
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

	S1 := []byte{111, 73, 155, 177, 61, 63, 23, 66, 114, 145, 169, 100, 42, 69, 29, 195, 19, 250, 206, 171, 75, 83, 125, 86, 63, 201, 45, 21, 118, 89, 46, 128}
	S2 := []byte{203, 197, 210, 190, 215, 22, 121, 210, 61, 110, 17, 192, 252, 227, 156, 118, 219, 255, 211, 227, 36, 59, 176, 201, 35, 81, 21, 147, 147, 143, 26, 125}
	
	S1Mixed := mixing(S1, sum, sum)
	S1Shuffle := shuffle(S1Mixed, S1Mixed)

	S2Mixed := mixing(S2, sum, sum)
	S2Shuffle := shuffle(S1Mixed, S2Mixed)

	var output []byte
	
	for block := 0; block < len(inputBlocks); block++ {
		var outputBlock []byte
		for b := 0; b < 32; b++ {
			outputByte := inputBlocks[block][b] ^ S1Shuffle[b] ^ (S2Shuffle[b] ^ inputBlocks[block][b])
			outputByte = (inputBlocks[block][b] ^ S1Mixed[b]) ^ outputByte // fixes collisions
			outputBlock = append(outputBlock, outputByte)
		}
		output = shuffle(outputBlock, input)
	}

	return output	
}

func main() {
    MODE := "FAST" // FAST or PSWD
	
    input := []byte("juh8odipasdasjuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasjuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardauosaodo2guaoisdrosardajuh8odipasdasjuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guasdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardauosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardauosaodo2guaoisdrosardasdasjuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardauosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardajuh8odipasdasuosaodo2guaoisdrosardauosaodo2guaoisdrosarda") // Example input
    startDec := time.Now()
    output := processing(input, MODE)
    durationDec := time.Since(startDec)
    fmt.Println("Output: ", output)
    fmt.Println("Operation took:", durationDec)
    fmt.Println(len(output))
}

//under dev