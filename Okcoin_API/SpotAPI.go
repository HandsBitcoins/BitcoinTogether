package main

import (
	"encoding/json"
	"log"
	"net/url"
	"strings"
)

import "fmt"

func tm() {
	fmt.Println("asd")
}

type SpotAPI struct {
	keysCrypted []byte
}

func (a *SpotAPI) Init() {
	if isNotExistKeys() {
		initFiles()
	}

	a.keysCrypted = checkPassword()
	if a.keysCrypted == nil {
		fmt.Println("\nWrong Password. Quit program.")
	}
}

func (a *SpotAPI) readKeys() []string {
	keyOTP := generateOneTimePassword()
	keys := strings.Split(string(decryptCBC(loadOneTimePassword(), a.keysCrypted)), "|")
	saveOneTimePassword(keyOTP)
	a.keysCrypted = encryptCBC(keyOTP, []byte(keys[0]+"|"+keys[1]))

	return keys
}

func GetPriceTicker(symbol bool) ResponsePriceTicker {
	params := url.Values{}
	addSymbolToParam(symbol, &params)

	var res ResponsePriceTicker
	err := json.Unmarshal(GetHTTP("/api/v1/ticker.do?", params), &res)
	if err != nil {
		log.Fatal(err)
	}

	return res
}

func GetMarketDepth(symbol bool) ResponseMarketDepth {
	params := url.Values{}
	addSymbolToParam(symbol, &params)

	var res ResponseMarketDepth
	err := json.Unmarshal(GetHTTP("/api/v1/depth.do?", params), &res)
	if err != nil {
		log.Fatal(err)
	}

	return res
}

func GetTradeRecently(symbol bool) ResponseTradeRecently {
	params := url.Values{}
	addSymbolToParam(symbol, &params)

	var res ResponseTradeRecently

	err := json.Unmarshal(GetHTTP("/api/v1/trades.do?", params), &res)
	if err != nil {
		log.Fatal(err)
	}

	return res
}

func GetCandlestickData(symbol bool, candleTime int) []ResponseCandlestickData {
	params := url.Values{}
	addSymbolToParam(symbol, &params)
	addCandleTimeToParam(candleTime, &params)

	var res []ResponseCandlestickData
	err := json.Unmarshal(GetHTTP("/api/v1/kline.do?", params), &res)
	if err != nil {
		log.Fatal(err)
	}

	return res
}

func (a *SpotAPI) GetUserAccountInfo() {
	params := url.Values{}
	params.Add("api_key", "e7ccc79a-6c2a-4cde-b82a-98b7b55b2cdf")
	params.Add("sign", buildMySign(params, "F8C0D0157B26D0D16E885AE57480D8CE"))
	//fmt.Println(params)

	/*
		resp, err := http.PostForm("https://www.okcoin.com/api/v1/userinfo.do", params)
		if err != nil {
			fmt.Println("err")
			log.Fatal(err)
		}

		contents, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			log.Fatal(err)
		}

		fmt.Println(string(contents))
		var srutResp ResponseUserInfo
		err = json.Unmarshal(contents, &srutResp)
		if err != nil {
			log.Fatal(err)
		}*/
}

/*
POST /api/v1/userinfo Get User Account Info
POST /api/v1/trade Place Orders
POST /api/v1/trade_history  New Get Trade History (Not for Personal)
POST /api/v1/batch_trade Batch Trade
POST /api/v1/cancel_order Cancel Orders
POST /api/v1/order_info Get Order Info
POST /api/v1/orders_info Get Order Information in Batch
POST /api/v1/order_history Only the most recent 7 days are returned
POST /api/v1/withdraw BTC/LTC Withdraw
POST /api/v1/cancel_withdraw Withdrawal Cancellation Request
POST /api/v1/withdraw_info  New Get Withdrawal Information
POST /api/v1/order_fee  New Query Fee
POST /api/v1/lend_depth  New Get Top 10 Lending Entries
POST /api/v1/borrows_info  New Get User Borrow Information
POST /api/v1/borrow_money  New Request Borrow
POST /api/v1/cancel_borrow  New Cancel Borrow Order
POST /api/v1/borrow_order_info  New Get Borrowing Order Info
POST /api/v1/repayment  New Pay Off Debt
POST /api/v1/unrepayments_info  New Get Debt List
POST /api/v1/account_records  New Get User Deposits or Withdraw Record*/
