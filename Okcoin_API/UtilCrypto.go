package main

import (
	"bytes"
	"crypto/aes"
	"crypto/cipher"
	"crypto/md5"
	crand "crypto/rand"
	"fmt"
	"io"
	"io/ioutil"
	"math"
	"math/rand"
	"os"
	"strconv"
	"strings"
	"syscall"
	"time"
	"unsafe"
)

const NAME_FILE_KEY_INFO = "OKcoinAPI.dat"
const NAME_FILE_SALT_BOOK = "SaltBook.dat"
const NAME_FILE_OTP = "lock"

const LENGTH_AES_KEY = 32
const LENGTH_SALT = 32
const NUMBER_SALT_ITEM = 128

const ENABLE_ECHO_INPUT = uint32(0x0004)

var kernel32 = syscall.NewLazyDLL("kernel32.dll")

var (
	procGetConsoleMode = kernel32.NewProc("GetConsoleMode")
	procSetConsoleMode = kernel32.NewProc("SetConsoleMode")
)

func isNotExistKeys() bool {
	_, err := os.Stat(NAME_FILE_KEY_INFO)
	return os.IsNotExist(err)
}

func setEchoWindowsConsole(enable bool) {
	stdInHandle, err := syscall.GetStdHandle(syscall.STD_INPUT_HANDLE)
	if err != nil {
		panic(fmt.Errorf("could not get standard io handle %d", stdInHandle))
	}

	var mode uint32
	procGetConsoleMode.Call(uintptr(stdInHandle), uintptr(unsafe.Pointer(&mode)))

	if enable {
		mode |= ENABLE_ECHO_INPUT
	} else {
		mode &= ^ENABLE_ECHO_INPUT
	}

	procSetConsoleMode.Call(uintptr(stdInHandle), uintptr(mode))
}

func initFiles() {
	makeSaltBook()

	pass, passConfirm, keyAPI, keySecret := new([]byte), new([]byte), new([]byte), new([]byte)
	setEchoWindowsConsole(false)
	fmt.Print("API key file not exist!!")
	fmt.Print("Set the excute password...")
	fmt.Print("Please enter a password: ")
	fmt.Scanf("%s", pass)
	fmt.Scanf("%s", pass)

	fmt.Print("\nReenter password to confirm: ")
	fmt.Scanf("%s", passConfirm)
	fmt.Scanf("%s", passConfirm)
	setEchoWindowsConsole(true)

	if strings.Compare(string(*pass), string(*passConfirm)) != 0 {
		fmt.Print("\nTwo passwords are different. Quit the program.")
		return
	}

	fmt.Print("\nPlease enter \"API_Key SecretKey\" at once: ")
	fmt.Scanf("%s %s", keyAPI, keySecret)

	writeEncryptCode(encryptCBC(extendKey(*pass), []byte(strings.Join([]string{string(*pass), string(*keyAPI), string(*keySecret)}, "|"))))

	//	sss := string(decryptCBC(keyExtended, enKA))
	//	fmt.Println(sss, strings.Contains(sss, string(*password)))
}

func checkPassword() []byte {
	pass := new([]byte)
	setEchoWindowsConsole(false)
	fmt.Print("Enter a password to execute: ")
	fmt.Scanf("%s", pass)
	fmt.Scanf("%s", pass)
	setEchoWindowsConsole(true)

	code := readEncryptCode()
	dataDecrypted := strings.Split(string(decryptCBC(extendKey(*pass), code)), "|")

	if strings.Compare(dataDecrypted[0], string(*pass)) != 0 {
		return nil
	}

	keyOTP := generateOneTimePassword()

	saveOneTimePassword(keyOTP)
	return encryptCBC(keyOTP, []byte(dataDecrypted[1]+"|"+dataDecrypted[2]))
}

func generateOneTimePassword() []byte {
	timeHash := md5.Sum([]byte(strconv.FormatInt(time.Now().UnixNano(), 10)))
	return append(readSaltBook(int(time.Now().UnixNano() % NUMBER_SALT_ITEM))[0:16], timeHash[:]...)
}

func getOneTimePassword() []byte {
	timeHash := md5.Sum([]byte(strconv.FormatInt(time.Now().UnixNano(), 10)))
	return append(getRandomSalt(), timeHash[:]...)
}

func saveOneTimePassword(key []byte) {
	f, err := os.Create(NAME_FILE_OTP)
	if err != nil {
		panic(err)
	}
	defer f.Close()

	f.Write(key)
}

func loadOneTimePassword() []byte {
	dat, err := ioutil.ReadFile(NAME_FILE_OTP)
	if err != nil {
		fmt.Println("Error with one time password file!!")
		panic(err)
	}

	return dat
}

func writeEncryptCode(code []byte) {
	f, err := os.Create(NAME_FILE_KEY_INFO)
	if err != nil {
		panic(err)
	}
	defer f.Close()

	f.Write(code)
}

func readEncryptCode() []byte {
	dat, err := ioutil.ReadFile(NAME_FILE_KEY_INFO)
	if err != nil {
		panic(err)
	}
	return dat
}

func makeSaltBook() {
	f, err := os.Create(NAME_FILE_SALT_BOOK)
	if err != nil {
		panic(err)
	}
	defer f.Close()

	for j := 0; j < NUMBER_SALT_ITEM; j++ {
		salt := getRandomSalt()
		f.Write(salt)
	}
}

func getRandomSalt() []byte {
	salt := make([]byte, LENGTH_SALT)
	for i := 0; i < LENGTH_SALT; i++ {
		salt[i] = byte(rand.Intn(math.MaxUint8 + 1))
	}
	return salt
}

func readSaltBook(index int) []byte {
	f, err := os.Open(NAME_FILE_SALT_BOOK)
	if err != nil {
		panic(err)
	}

	_, err = f.Seek(int64(index*LENGTH_SALT), 0)
	if err != nil {
		panic(err)
	}

	salt := make([]byte, LENGTH_SALT)
	_, err = f.Read(salt)
	if err != nil {
		panic(err)
	}

	f.Close()

	return salt
}

func extendKey(key []byte) []byte {
	return append(key, readSaltBook(getSaltIndex(key))...)[0:LENGTH_AES_KEY]
}

func getSaltIndex(key []byte) int {
	hash := md5.Sum(key)

	sumHash := 0
	for i := 0; i < len(hash); i++ {
		sumHash += int(hash[i])
	}

	return sumHash % NUMBER_SALT_ITEM
}

func encryptCBC(key []byte, plaintext []byte) []byte {
	leftLength := len(plaintext) % aes.BlockSize
	if len(plaintext)%aes.BlockSize != 0 {
		for i := 0; i < (aes.BlockSize - leftLength); i++ {
			plaintext = append(plaintext, 0)
		}
	}

	block, err := aes.NewCipher(key)
	if err != nil {
		panic(err)
	}

	ciphertext := make([]byte, aes.BlockSize+len(plaintext))
	iv := ciphertext[:aes.BlockSize]
	if _, err := io.ReadFull(crand.Reader, iv); err != nil {
		panic(err)
	}

	mode := cipher.NewCBCEncrypter(block, iv)
	mode.CryptBlocks(ciphertext[aes.BlockSize:], plaintext)

	return ciphertext
}

func decryptCBC(key []byte, ciphertext []byte) []byte {
	block, err := aes.NewCipher(key)
	if err != nil {
		panic(err)
	}

	if len(ciphertext) < aes.BlockSize {
		panic("ciphertext too short")
	}
	iv := ciphertext[:aes.BlockSize]
	ciphertext = ciphertext[aes.BlockSize:]

	if len(ciphertext)%aes.BlockSize != 0 {
		panic("ciphertext is not a multiple of the block size")
	}

	mode := cipher.NewCBCDecrypter(block, iv)

	mode.CryptBlocks(ciphertext, ciphertext)

	ciphertext = bytes.Trim(ciphertext, "\x00")

	return ciphertext
}
