// Forest
package main

import "fmt"
import "sort"
import "math/rand"

type Forest struct {
	learners             []Learner
	counterEvaluate      int
	nextEvaluateDuration int
	lastID               int
}

type ByTotalBalance []Learner

func (b ByTotalBalance) Len() int           { return len(b) }
func (b ByTotalBalance) Swap(i, j int)      { b[i], b[j] = b[j], b[i] }
func (b ByTotalBalance) Less(i, j int) bool { return b[i].getTotalBalance() > b[j].getTotalBalance() }

const NUM_LEARNERS = 500
const MAX_DURATION_EVALUATE = 18000 * 24 * 7

func (f *Forest) Init() {
	f.learners = make([]Learner, NUM_LEARNERS)
	f.counterEvaluate = 0
	f.nextEvaluateDuration = rand.Intn(MAX_DURATION_EVALUATE)
	for i, _ := range f.learners {
		f.learners[i].Init(f.lastID)
		f.lastID++
	}
}

func (f *Forest) Execute(values []float64, price float64) {
	for i, _ := range f.learners {
		f.learners[i].execute(values, price)
	}

	f.counterEvaluate++
	if f.counterEvaluate == f.nextEvaluateDuration {
		f.Evaluate(price)
		f.Crossover()
		f.Mutate()
		f.AddNewLearner()

		f.nextEvaluateDuration = rand.Intn(MAX_DURATION_EVALUATE)
		f.counterEvaluate = 0
	}
}

func (f *Forest) Evaluate(price float64) {
	sort.Sort(ByTotalBalance(f.learners))

	f.learners = f.learners[0 : NUM_LEARNERS/10]

	base := 7000.0/price + 10.0
	fmt.Println("base:", base, price, f.nextEvaluateDuration)
	for i := 0; i < 10; i++ {
		totalBalance := f.learners[i].getTotalBalance()
		if totalBalance > base {
			fmt.Println("     ", i, f.learners[i].id, f.learners[i].typeGene, len(f.learners[i].chromosome.coeff[0]), len(f.learners[i].chromosome.coeff[1]), len(f.learners[i].chromosome.coeff[2]), len(f.learners[i].chromosome.coeff[3]), f.learners[i].chromosome.constant)
			fmt.Println("     ", i, f.learners[i].id, totalBalance, (totalBalance-base)/base*100.0/(float64(f.nextEvaluateDuration)/432000.0), f.learners[i].balanceBit, f.learners[i].balanceDollar, f.learners[i].counterBuy, f.learners[i].counterSell)
		}
	}

	for i := 0; i < NUM_LEARNERS/10; i++ {
		f.learners[i].reset()
	}
}

func (f *Forest) Crossover() {
	crossLearners := make([]Learner, NUM_LEARNERS/10*3)
	i, j := 0, 1
	for accum := 0; accum < NUM_LEARNERS/10*3; accum++ {
		crossLearners[accum].InitCrossover([]Learner{f.learners[i], f.learners[j]}, f.lastID)
		f.lastID++
		if j != NUM_LEARNERS/10-1 {
			j++
		} else {
			if i != NUM_LEARNERS/10-2 {
				i++
				j = i + 1
			} else {
				i, j = 0, 1
			}
		}
	}

	f.learners = append(f.learners, crossLearners...)
}

func (f *Forest) Mutate() {
	populNow := len(f.learners)
	mutLearners := make([]Learner, populNow)

	for i := 0; i < populNow; i++ {
		mutLearners[i].InitMuatation(f.learners[i], f.lastID)
		f.lastID++
	}

	f.learners = append(f.learners, mutLearners...)
}

func (f *Forest) AddNewLearner() {
	newLearners := make([]Learner, NUM_LEARNERS-len(f.learners))
	for i, _ := range newLearners {
		newLearners[i].Init(f.lastID)
		f.lastID++
	}
	f.learners = append(f.learners, newLearners...)
}
