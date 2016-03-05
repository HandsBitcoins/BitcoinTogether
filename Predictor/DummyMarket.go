// DummyMarket
package main

import (
	"math"
	"math/rand"
	"time"
)

type Market struct {
	price   float64
	counter float64
}

func (m *Market) Init() {
	rand.Seed(time.Now().UTC().UnixNano())
	m.price = 400.0
	m.counter = 0.0
}

func (m *Market) GetMarketPrice() float64 {
	m.price += rand.NormFloat64() * 0.01
	if rand.Int31n(200) == 0 {
		m.price += math.Cos(math.Pi*m.counter/180) * 2.0
		m.counter += 30.0
	}

	return m.price
}
