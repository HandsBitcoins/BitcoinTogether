// main
package main

import (
	"crypto/md5"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"math/rand"
	"net/http"
	"net/url"
	"sort"
	"strings"
	"time"
)

func addSymbolToParam(symbol bool, params *url.Values) {
	if symbol {
		params.Add("symbol", "btc_usd")
	} else {
		params.Add("symbol", "ltc_usd")
	}
}

func addCandleTimeToParam(candleTime int, params *url.Values) {
	switch candleTime {
	case CANDLE_TIME_1_MIN:
		params.Add("type", "1min")
	case CANDLE_TIME_3_MIN:
		params.Add("type", "3min")
	case CANDLE_TIME_5_MIN:
		params.Add("type", "5min")
	case CANDLE_TIME_15_MIN:
		params.Add("type", "15min")
	case CANDLE_TIME_30_MIN:
		params.Add("type", "30min")
	case CANDLE_TIME_1_HOUR:
		params.Add("type", "1hour")
	case CANDLE_TIME_2_HOUR:
		params.Add("type", "2hour")
	case CANDLE_TIME_4_HOUR:
		params.Add("type", "4hour")
	case CANDLE_TIME_6_HOUR:
		params.Add("type", "6hour")
	case CANDLE_TIME_12_HOUR:
		params.Add("type", "12hour")
	case CANDLE_TIME_1_DAY:
		params.Add("type", "1day")
	case CANDLE_TIME_3_DAY:
		params.Add("type", "3day")
	case CANDLE_TIME_1_WEEK:
		params.Add("type", "1week")
	default:
		params.Add("type", "5min")
	}
}

func (r *ResponseCandlestickData) UnmarshalJSON(contentJSON []byte) error {
	tmp := []interface{}{&r.Timestamp, &r.Open, &r.High, &r.Low, &r.Close, &r.Volume}
	wantLen := len(tmp)
	if err := json.Unmarshal(contentJSON, &tmp); err != nil {
		return err
	}
	if g, e := len(tmp), wantLen; g != e {
		return fmt.Errorf("wrong number of fields in Notification: %d != %d", g, e)
	}
	return nil
}

func buildMySign(params url.Values, secretKey string) string {
	var sign string

	var keys []string
	for k := range params {
		keys = append(keys, k)
	}
	sort.Strings(keys)

	for _, key := range keys {
		sign += key + "=" + params[key][0] + "&"
	}

	valueMD5 := md5.Sum([]byte(sign + "secret_key=" + secretKey))

	return strings.ToUpper(hex.EncodeToString(valueMD5[:]))
}

func GetHTTP(subURL string, params url.Values) []byte {
	resp, err := http.Get(DEFAULT_URL + subURL + params.Encode())
	if err != nil {
		log.Fatal(err)
	}

	contents, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}

	return contents
}

func main() {
	fmt.Println("Start")

	rand.Seed(time.Now().UnixNano())

	var sAPI SpotAPI
	sAPI.Init()
	/*
		params := url.Values{}
		params.Add("api_key", "e7ccc79a-6c2a-4cde-b82a-98b7b55b2cdf")
		params.Add("sign", buildMySign(params, "F8C0D0157B26D0D16E885AE57480D8CE"))
		//fmt.Println(params)

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

	//fmt.Println(GetPriceTicker(SYMBOL_BTC_USD))
	//fmt.Println(GetMarketDepth(SYMBOL_BTC_USD))
	//fmt.Println(GetTradeRecently(SYMBOL_BTC_USD))
	//fmt.Println(GetCandlestickData(SYMBOL_BTC_USD, CANDLE_TIME_1_DAY))
}
