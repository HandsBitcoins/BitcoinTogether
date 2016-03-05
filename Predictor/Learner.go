// Learner
package main

import (
	"math"
	"math/rand"
)

const SIGNAL_BUY = 1
const SIGNAL_KEEP = 0
const SIGNAL_SELL = -1

const NUM_GENE_INPUT_VALUES = 4

const AMPLIFIER_COEFF_RAND = 5.0

type gene struct {
	coeff    [NUM_GENE_INPUT_VALUES][]float64
	constant float64
}

type Learner struct {
	id         int
	typeGene   int
	chromosome gene

	balanceBit       float64
	balanceDollar    float64
	prevDifferential float64
	prevPrice        float64
	counterBuy       int
	counterSell      int
}

func (g *gene) Init() {
	for i := 0; i < NUM_GENE_INPUT_VALUES; i++ {
		g.coeff[i] = make([]float64, 1)
		g.coeff[i][0] = rand.NormFloat64() * AMPLIFIER_COEFF_RAND
	}
	g.constant = rand.NormFloat64() * AMPLIFIER_COEFF_RAND
}

func (g *gene) InitCrossover(p []gene) {
	for i := 0; i < NUM_GENE_INPUT_VALUES; i++ {
		selectedP := rand.Intn(2)
		g.coeff[i] = make([]float64, len(p[selectedP].coeff[i]))
		copy(g.coeff[i], p[selectedP].coeff[i])
	}
	g.constant = p[rand.Intn(2)].constant
}

func (g *gene) InitMuatation(src gene) {
	for i := 0; i < NUM_GENE_INPUT_VALUES; i++ {
		g.coeff[i] = make([]float64, len(src.coeff[i]))
		copy(g.coeff[i], src.coeff[i])
	}
	g.constant = src.constant

	//select index of value
	indexMutatingValue := rand.Intn(NUM_GENE_INPUT_VALUES)

	if rand.Intn(2) == 0 {
		//mutate order
		if rand.Intn(2) == 0 {
			//increase order
			g.coeff[indexMutatingValue] = append(g.coeff[indexMutatingValue], rand.NormFloat64()*AMPLIFIER_COEFF_RAND)
		} else {
			//decrease order
			orderNow := len(g.coeff[indexMutatingValue])
			if orderNow > 1 {
				g.coeff[indexMutatingValue] = g.coeff[indexMutatingValue][0 : orderNow-1]
			}
		}

	} else {
		//mutate coeff
		orderSelected := rand.Intn(len(g.coeff[indexMutatingValue]))
		g.coeff[indexMutatingValue][orderSelected] += rand.NormFloat64() * 0.1
	}

}

func (g gene) calculate(values []float64) (float64, float64) {
	signalRaw := g.constant

	for i, _ := range g.coeff {
		base := 1.0
		for j, _ := range g.coeff[i] {
			base *= values[i]
			signalRaw += g.coeff[i][j] * base
		}
	}

	return math.Atan(signalRaw), 1.0 / signalRaw / signalRaw
}

func (l *Learner) Init(id int) {
	l.id = id
	l.typeGene = 0
	l.reset()
	l.chromosome.Init()
}

func (l *Learner) InitCrossover(p []Learner, id int) {
	l.id = id
	l.typeGene = 1
	l.reset()
	l.chromosome.InitCrossover([]gene{p[0].chromosome, p[1].chromosome})
}

func (l *Learner) InitMuatation(src Learner, id int) {
	l.id = id
	l.typeGene = 2
	l.reset()
	l.chromosome.InitMuatation(src.chromosome)
}

func (l *Learner) judge(values []float64) (int, float64) {
	signal, diffSignal := l.chromosome.calculate(values)
	order := SIGNAL_KEEP

	if signal < 0 {
		order = SIGNAL_SELL
	} else if signal > 0 {
		order = SIGNAL_BUY
	}

	l.prevDifferential = diffSignal

	return order, signal
}

func (l *Learner) judgeStrict(values []float64) (int, float64) {
	signal, diffSignal := l.chromosome.calculate(values)
	order := SIGNAL_KEEP

	if (diffSignal > 0) && (l.prevDifferential < 0) && (signal < 0) {
		order = SIGNAL_SELL
	} else if (diffSignal < 0) && (l.prevDifferential > 0) && (signal > 0) {
		order = SIGNAL_BUY
	}

	l.prevDifferential = diffSignal

	return order, signal
}

func (l *Learner) execute(values []float64, price float64) {
	order, _ := l.judge(values)
	if order == SIGNAL_BUY {
		if l.balanceDollar > price {
			l.balanceBit += 1.0 / 1.002
			l.balanceDollar -= price
			l.counterBuy++
			//fmt.Println("buy", l.balanceBit, l.balanceDollar)
		}
	} else if order == SIGNAL_SELL {
		if l.balanceBit >= 1.0 {
			l.balanceBit -= 1.0
			l.balanceDollar += price / 1.002
			l.counterSell++

			//fmt.Println("Sell", l.balanceBit, l.balanceDollar)
		}
	}

	l.prevPrice = price
}

func (l Learner) getTotalBalance() float64 {
	return l.balanceBit + (l.balanceDollar / l.prevPrice)
}

func (l *Learner) reset() {
	l.balanceBit = 10.0
	l.balanceDollar = 7000.0
	l.counterBuy = 0
	l.counterSell = 0
}
