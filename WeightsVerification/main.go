package main

import (
	"fmt"

	"github.com/consensys/gnark-crypto/ecc"
	"github.com/consensys/gnark/backend/groth16"
	"github.com/consensys/gnark/frontend"
	"github.com/consensys/gnark/frontend/cs/r1cs"
)

// Sigmoid function approximation using a polynomial
func sigmoid(api frontend.API, x frontend.Variable) frontend.Variable {
	one := frontend.Variable(1)
	// Approximate sigmoid using 1 / (1 + exp(-x)) ≈ 1 / (1 + (1 - x + x^2/2))
	approxExpNegX := api.Add(one, api.Sub(x, api.Div(api.Mul(x, x), frontend.Variable(2))))
	return api.Div(one, approxExpNegX)
}

// LogisticRegressionCircuit defines a simple logistic regression model

func (circuit *ProveModelCircuit) Define(api frontend.API) error {
	nFeatures := len(circuit.FeatureValues)
	sum := circuit.Bias

	// Compute linear combination: sum = w1*x1 + w2*x2 + ... + wn*xn + bias
	for i := 0; i < nFeatures; i++ {
		weightedFeature := api.Mul(circuit.FeatureValues[i], circuit.Weights[i])
		sum = api.Add(sum, weightedFeature)
	}

	// Apply sigmoid function approximation
	probability := sigmoid(api, sum)

	// Threshold at 0.5 for classification (0 or 1)
	threshold := frontend.Variable(5)
	classPrediction := api.Cmp(probability, threshold)
	api.AssertIsEqual(classPrediction, circuit.Prediction)

	return nil
}

type ProveModelCircuit struct {
	FeatureValues [2]frontend.Variable `gnark:",private"`
	Weights       [2]frontend.Variable `gnark:",private"`
	Bias          frontend.Variable    `gnark:",private"`
	Prediction    frontend.Variable    `gnark:",private"`
}

func main() {
	// Compile the logistic regression circuit
	var logRegCircuit ProveModelCircuit
	r1cs, err := frontend.Compile(ecc.BN254.ScalarField(), r1cs.NewBuilder, &logRegCircuit)
	if err != nil {
		fmt.Println("Error compiling circuit:", err)
		return
	}

	// Generate zk-SNARK proving and verification keys
	pk, vk, err := groth16.Setup(r1cs)
	if err != nil {
		fmt.Println("Error during setup:", err)
		return
	}

	// Example feature values, weights, bias, and expected prediction
	assignment := &ProveModelCircuit{}
	assignment.FeatureValues[0] = 20
	assignment.FeatureValues[1] = 30
	assignment.Weights[0] = 5
	assignment.Weights[1] = -2
	assignment.Bias = 1
	assignment.Prediction = 1
	// Generate proof
	fmt.Print(assignment)
	witness, err := frontend.NewWitness(assignment, ecc.BN254.ScalarField())
	if err != nil {
		fmt.Println("Error creating witness:", err)
		return
	}

	proof, err := groth16.Prove(r1cs, pk, witness)
	if err != nil {
		fmt.Println("Error proving:", err)
		return
	}

	// Verify proof
	publicWitness, err := witness.Public()
	if err != nil {
		fmt.Println("Error getting public witness:", err)
		return
	}

	err = groth16.Verify(proof, vk, publicWitness)
	if err != nil {
		fmt.Println("Verification failed")
	} else {
		fmt.Println("Verification succeeded")
	}
}
