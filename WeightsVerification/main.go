// package main

// import (
// 	"fmt"

// 	"github.com/consensys/gnark-crypto/ecc"
// 	"github.com/consensys/gnark/backend/groth16"
// 	"github.com/consensys/gnark/frontend"
// 	"github.com/consensys/gnark/frontend/cs/r1cs"
// )

// // Sigmoid function approximation using a polynomial
// func sigmoid(api frontend.API, x frontend.Variable) frontend.Variable {
// 	one := frontend.Variable(1)
// 	// Approximate sigmoid using 1 / (1 + exp(-x)) ≈ 1 / (1 + (1 - x + x^2/2))
// 	approxExpNegX := api.Add(one, api.Sub(x, api.Div(api.Mul(x, x), frontend.Variable(2))))
// 	return api.Div(one, approxExpNegX)
// }

// // LogisticRegressionCircuit defines a simple logistic regression model

// func (circuit *ProveModelCircuit) Define(api frontend.API) error {
// 	nFeatures := len(circuit.FeatureValues)
// 	sum := circuit.Bias

// 	// Compute linear combination: sum = w1*x1 + w2*x2 + ... + wn*xn + bias
// 	for i := 0; i < nFeatures; i++ {
// 		weightedFeature := api.Mul(circuit.FeatureValues[i], circuit.Weights[i])
// 		sum = api.Add(sum, weightedFeature)
// 	}

// 	// Apply sigmoid function approximation
// 	probability := sigmoid(api, sum)

// 	// Threshold at 0.5 for classification (0 or 1)
// 	threshold := frontend.Variable(5)
// 	classPrediction := api.Cmp(probability, threshold)
// 	api.AssertIsEqual(classPrediction, circuit.Prediction)

// 	return nil
// }

// type ProveModelCircuit struct {
// 	FeatureValues [2]frontend.Variable `gnark:",private"`
// 	Weights       [2]frontend.Variable `gnark:",private"`
// 	Bias          frontend.Variable    `gnark:",private"`
// 	Prediction    frontend.Variable    `gnark:",private"`
// }

// func main() {
// 	// Compile the logistic regression circuit
// 	var logRegCircuit ProveModelCircuit
// 	r1cs, err := frontend.Compile(ecc.BN254.ScalarField(), r1cs.NewBuilder, &logRegCircuit)
// 	if err != nil {
// 		fmt.Println("Error compiling circuit:", err)
// 		return
// 	}

// 	// Generate zk-SNARK proving and verification keys
// 	pk, vk, err := groth16.Setup(r1cs)
// 	if err != nil {
// 		fmt.Println("Error during setup:", err)
// 		return
// 	}

// 	// Example feature values, weights, bias, and expected prediction
// 	assignment := &ProveModelCircuit{}
// 	assignment.FeatureValues[0] = 20
// 	assignment.FeatureValues[1] = 30
// 	assignment.Weights[0] = 5
// 	assignment.Weights[1] = -2
// 	assignment.Bias = 1
// 	assignment.Prediction = 1
// 	// Generate proof
// 	fmt.Print(assignment)
// 	witness, err := frontend.NewWitness(assignment, ecc.BN254.ScalarField())
// 	if err != nil {
// 		fmt.Println("Error creating witness:", err)
// 		return
// 	}

// 	proof, err := groth16.Prove(r1cs, pk, witness)
// 	if err != nil {
// 		fmt.Println("Error proving:", err)
// 		return
// 	}

// 	// Verify proof
// 	publicWitness, err := witness.Public()
// 	if err != nil {
// 		fmt.Println("Error getting public witness:", err)
// 		return
// 	}

//		err = groth16.Verify(proof, vk, publicWitness)
//		if err != nil {
//			fmt.Println("Verification failed")
//		} else {
//			fmt.Println("Verification succeeded")
//		}
//	}

// package main

// import (
// 	"fmt"

// 	"github.com/consensys/gnark-crypto/ecc"
// 	"github.com/consensys/gnark/backend/groth16"
// 	"github.com/consensys/gnark/frontend"
// 	"github.com/consensys/gnark/frontend/cs/r1cs"
// )

// // Decision Tree Node - Approximating a Decision Tree in zk-SNARKs
// func decisionTree(api frontend.API, feature1, feature2 frontend.Variable) frontend.Variable {
// 	threshold1 := frontend.Variable(15)
// 	threshold2 := frontend.Variable(25)

// 	// First split: if feature1 > 15
// 	leftBranch := api.Cmp(feature1, threshold1)

// 	// Second split: if feature2 > 25
// 	rightBranch := api.Cmp(feature2, threshold2)

// 	// Decision: If leftBranch == 1 and rightBranch == 1 → Class 1, else Class 0
// 	prediction := api.Mul(leftBranch, rightBranch) // This ensures both conditions are met
// 	return prediction
// }

// // RandomForestCircuit - An approximation of a 3-tree Random Forest
// type RandomForestCircuit struct {
// 	FeatureValues [2]frontend.Variable `gnark:",private"`
// 	Prediction    frontend.Variable    `gnark:",public"`
// }

// func (circuit *RandomForestCircuit) Define(api frontend.API) error {
// 	// Define three decision trees (simplified)
// 	tree1 := decisionTree(api, circuit.FeatureValues[0], circuit.FeatureValues[1])
// 	tree2 := decisionTree(api, circuit.FeatureValues[0], api.Add(circuit.FeatureValues[1], frontend.Variable(5)))
// 	tree3 := decisionTree(api, api.Add(circuit.FeatureValues[0], frontend.Variable(-3)), circuit.FeatureValues[1])

// 	// Majority Voting: Sum of tree outputs should be >= 2 for class 1, else class 0
// 	sumPredictions := api.Add(api.Add(tree1, tree2), tree3)
// 	finalPrediction := api.Cmp(sumPredictions, frontend.Variable(2)) // If at least 2 trees vote "1", final class is 1
// 	api.Println("This is the final predictinp", finalPrediction)
// 	// Ensure that the computed prediction matches the expected prediction
// 	api.AssertIsEqual(finalPrediction, circuit.Prediction)

// 	return nil
// }

// func main() {
// 	// Compile the Random Forest circuit
// 	var rfCircuit RandomForestCircuit
// 	r1cs, err := frontend.Compile(ecc.BN254.ScalarField(), r1cs.NewBuilder, &rfCircuit)
// 	if err != nil {
// 		fmt.Println("Error compiling circuit:", err)
// 		return
// 	}

// 	// Generate zk-SNARK proving and verification keys
// 	pk, vk, err := groth16.Setup(r1cs)
// 	if err != nil {
// 		fmt.Println("Error during setup:", err)
// 		return
// 	}

// 	// Example feature values and expected prediction
// 	assignment := &RandomForestCircuit{}
// 	assignment.FeatureValues[0] = 20 // Example feature 1
// 	assignment.FeatureValues[1] = 30 // Example feature 2
// 	assignment.Prediction = 1        // Expected majority class

// 	// Generate witness
// 	witness, err := frontend.NewWitness(assignment, ecc.BN254.ScalarField())
// 	if err != nil {
// 		fmt.Println("Error creating witness:", err)
// 		return
// 	}

// 	// Generate proof
// 	proof, err := groth16.Prove(r1cs, pk, witness)
// 	if err != nil {
// 		fmt.Println("Error proving:", err)
// 		return
// 	}

// 	// Verify proof
// 	publicWitness, err := witness.Public()
// 	if err != nil {
// 		fmt.Println("Error getting public witness:", err)
// 		return
// 	}

//		err = groth16.Verify(proof, vk, publicWitness)
//		if err != nil {
//			fmt.Println("Verification failed")
//		} else {
//			fmt.Println("Verification succeeded")
//		}
//	}
package main

import (
	"fmt"

	"github.com/consensys/gnark-crypto/ecc"
	"github.com/consensys/gnark/backend/groth16"
	"github.com/consensys/gnark/frontend"
	"github.com/consensys/gnark/frontend/cs/r1cs"
)

// DecisionTreeRegression - Simulates a decision tree in zk-SNARKs
func DecisionTreeRegression(api frontend.API, feature1, feature2 frontend.Variable) frontend.Variable {
	// Decision thresholds (fixed for simplicity)
	threshold1 := frontend.Variable(15)
	threshold2 := frontend.Variable(25)

	// Fixed leaf values (simulated tree outputs)
	output1 := frontend.Variable(50) // If feature1 > 15 & feature2 > 25
	output2 := frontend.Variable(30) // If feature1 > 15 & feature2 ≤ 25
	output3 := frontend.Variable(20) // If feature1 ≤ 15 & feature2 > 25
	output4 := frontend.Variable(10) // If feature1 ≤ 15 & feature2 ≤ 25

	// Decision logic
	leftBranch := api.Cmp(feature1, threshold1)  // 1 if feature1 > 15
	rightBranch := api.Cmp(feature2, threshold2) // 1 if feature2 > 25

	// Select output based on feature splits
	treeOutput := api.Select(leftBranch,
		api.Select(rightBranch, output1, output2), // If leftBranch == 1, pick between output1/output2
		api.Select(rightBranch, output3, output4)) // If leftBranch == 0, pick between output3/output4

	return treeOutput
}

// RandomForestRegressionCircuit - zk-SNARK circuit for Random Forest Regression
type RandomForestRegressionCircuit struct {
	FeatureValues [2]frontend.Variable `gnark:",private"` // Input features
	MinValue      frontend.Variable    `gnark:",public"`  // Lower bound for valid prediction
	MaxValue      frontend.Variable    `gnark:",public"`  // Upper bound for valid prediction
	Prediction    frontend.Variable    `gnark:",public"`  // Computed prediction
}

// Define the zk-SNARK circuit
func (circuit *RandomForestRegressionCircuit) Define(api frontend.API) error {
	// Simulate 3 decision trees
	tree1 := DecisionTreeRegression(api, circuit.FeatureValues[0], circuit.FeatureValues[1])
	tree2 := DecisionTreeRegression(api, api.Add(circuit.FeatureValues[0], frontend.Variable(3)), circuit.FeatureValues[1])
	tree3 := DecisionTreeRegression(api, circuit.FeatureValues[0], api.Add(circuit.FeatureValues[1], frontend.Variable(-2)))

	// Compute final prediction (average of tree outputs)
	forestOutput := api.Div(api.Add(api.Add(tree1, tree2), tree3), frontend.Variable(3))

	// Ensure the computed prediction matches the expected Prediction

	// Ensure prediction falls within the expected range: MinValue ≤ Prediction ≤ MaxValue
	api.AssertIsLessOrEqual(circuit.MinValue, forestOutput)
	api.AssertIsLessOrEqual(forestOutput, circuit.MaxValue)

	return nil
}

func main() {
	// Define the zk-SNARK circuit
	var rfCircuit RandomForestRegressionCircuit
	r1cs, err := frontend.Compile(ecc.BN254.ScalarField(), r1cs.NewBuilder, &rfCircuit)
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

	// Define feature values and expected prediction range
	assignment := &RandomForestRegressionCircuit{}
	assignment.FeatureValues[0] = 20 // Feature 1
	assignment.FeatureValues[1] = 30 // Feature 2
	assignment.MinValue = 25         // Lower bound
	assignment.MaxValue = 55         // Upper bound
	assignment.Prediction = 50       // Expected Random Forest prediction

	// Generate witness
	witness, err := frontend.NewWitness(assignment, ecc.BN254.ScalarField())
	if err != nil {
		fmt.Println("Error creating witness:", err)
		return
	}

	// Generate proof
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
		fmt.Println("❌ Verification failed")
	} else {
		fmt.Println("✅ Verification succeeded")
	}
}
