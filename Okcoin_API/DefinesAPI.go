package main

const DEFAULT_URL = "https://www.okcoin.com"

const SYMBOL_BTC_USD = true
const SYMBOL_LTC_USD = false

const CANDLE_TIME_1_MIN = 0
const CANDLE_TIME_3_MIN = 1
const CANDLE_TIME_5_MIN = 2
const CANDLE_TIME_15_MIN = 3
const CANDLE_TIME_30_MIN = 4
const CANDLE_TIME_1_HOUR = 5
const CANDLE_TIME_2_HOUR = 6
const CANDLE_TIME_4_HOUR = 7
const CANDLE_TIME_6_HOUR = 8
const CANDLE_TIME_12_HOUR = 9
const CANDLE_TIME_1_DAY = 10
const CANDLE_TIME_3_DAY = 11
const CANDLE_TIME_1_WEEK = 12

type ResponsePriceTicker struct {
	Date   int64 `json:"date,string"`
	Ticker struct {
		Buy  float64 `json:"buy,string"`
		High float64 `json:"high,string"`
		Last float64 `json:"last,string"`
		Low  float64 `json:"low,string"`
		Sell float64 `json:"sell,string"`
		Vol  float64 `json:"vol,string"`
	} `json:"ticker"`
}

type ResponseMarketDepth struct {
	Asks [][]float64 `json:"asks"`
	Bids [][]float64 `json:"bids"`
}

type ResponseTradeRecently []struct {
	Date   int     `json:"date"`
	DateMs int64   `json:"date_ms"`
	Price  float64 `json:"price,string"`
	Amount float64 `json:"amount,string"`
	Tid    int     `json:"tid"`
	Type   string  `json:"type"`
}

type ResponseCandlestickData struct {
	Timestamp int64   `json:"0"`
	Open      float64 `json:"1"`
	High      float64 `json:"2"`
	Low       float64 `json:"3"`
	Close     float64 `json:"4"`
	Volume    float64 `json:"5"`
}

type ResponseUserInfo struct {
	Info struct {
		Funds struct {
			Asset struct {
				Net   float64 `json:"net,string"`
				Total float64 `json:"total,string"`
			} `json:"asset"`
			Borrow struct {
				Btc float64 `json:"btc,string"`
				Usd float64 `json:"usd,string"`
				Ltc float64 `json:"ltc,string"`
			} `json:"borrow"`
			Free struct {
				Btc float64 `json:"btc,string"`
				Usd float64 `json:"usd,string"`
				Ltc float64 `json:"ltc,string"`
			} `json:"free"`
			Freezed struct {
				Btc float64 `json:"btc,string"`
				Usd float64 `json:"usd,string"`
				Ltc float64 `json:"ltc,string"`
			} `json:"freezed"`
			UnionFund struct {
				Btc float64 `json:"btc,string"`
				Ltc float64 `json:"ltc,string"`
			} `json:"union_fund"`
		} `json:"funds"`
	} `json:"info"`
	Result bool `json:"result"`
}
