// MathTools
package main

import "math"

const DIVIDER_8_HOUR = 144000
const DIVIDER_11_HOUR = 198000
const DIVIDER_24_HOUR = 432000

const INDEX_END_OF_11HOUR = DIVIDER_24_HOUR - DIVIDER_11_HOUR

const LENGTH_DATA_MACD = DIVIDER_8_HOUR
const LENGTH_DATA_PRICE = DIVIDER_24_HOUR

type SingleData struct {
	timestmap int64
	data      float64
}

type Mathematician struct {
	dataMACD       []SingleData
	dataPrice      []SingleData
	dataOscillator []SingleData

	sumMV8  float64
	sumMV11 float64
	sumMV24 float64

	counter int

	enable bool
}

func (m *Mathematician) Init() {
	m.dataMACD = make([]SingleData, LENGTH_DATA_MACD)
	m.dataPrice = make([]SingleData, LENGTH_DATA_PRICE)
	m.dataOscillator = make([]SingleData, 2)

	m.counter = 0
	m.enable = false
}

func (m *Mathematician) UpdatePrice(price SingleData) {
	var out8, out11, out24 float64 = 0.0, 0.0, 0.0

	//------------------Calculate Price Moving Average-------------------
	if (m.counter > DIVIDER_11_HOUR-1) || m.enable {
		out11 = m.dataPrice[INDEX_END_OF_11HOUR].data
	}

	if (m.counter > DIVIDER_24_HOUR-1) || m.enable {
		out24 = m.dataPrice[0].data
	}

	m.dataPrice = append(m.dataPrice[1:LENGTH_DATA_PRICE], price)

	m.sumMV11 += price.data - out11
	m.sumMV24 += price.data - out24

	mv11 := m.sumMV11 / float64(DIVIDER_11_HOUR)
	mv24 := m.sumMV24 / float64(DIVIDER_24_HOUR)

	//------------------Calculate MACD Moving Average-------------------
	if (m.counter > DIVIDER_8_HOUR-1) || m.enable {
		out8 = m.dataMACD[0].data
	}

	m.dataMACD = append(m.dataMACD[1:LENGTH_DATA_MACD],
		SingleData{data: mv11 - mv24, timestmap: price.timestmap})
	m.sumMV8 += m.dataMACD[LENGTH_DATA_MACD-1].data - out8

	m.dataOscillator = append(m.dataOscillator[1:2],
		SingleData{
			data:      m.dataMACD[LENGTH_DATA_MACD-1].data - m.sumMV8/float64(DIVIDER_8_HOUR),
			timestmap: price.timestmap})

	//fmt.Println(sum-m.sumMV24, sum, m.sumMV24, sum/float64(DIVIDER_24_HOUR))
	//fmt.Println(m.counter, price.data, mv11, mv24, m.sumMV8/float64(DIVIDER_8_HOUR))
	m.counter++
}

func (m *Mathematician) IsEnable() bool {
	if m.enable {
		return true
	} else {
		m.enable = m.counter > DIVIDER_8_HOUR+DIVIDER_24_HOUR
		return m.enable
	}
}

func (m Mathematician) GetValues() []float64 {
	setValue := append(make([]float64, 0), m.dataMACD[LENGTH_DATA_MACD-1].data)
	setValue = append(setValue, getConvertedDifferential(m.dataMACD[LENGTH_DATA_MACD-2:LENGTH_DATA_MACD]))
	setValue = append(setValue, m.dataOscillator[1].data)
	setValue = append(setValue, getConvertedDifferential(m.dataOscillator[0:2]))

	return setValue
}

func getConvertedDifferential(dataSet []SingleData) float64 {
	// 1 / f'(x) + 1 = dt/(dp+dt)
	return math.Atan((dataSet[1].data - dataSet[0].data) / (float64(dataSet[1].timestmap-dataSet[0].timestmap) / 1000000000000))
}
