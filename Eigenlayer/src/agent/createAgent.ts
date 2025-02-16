import { OpacityAdapter } from '@layr-labs/agentkit-opacity';
import { EigenDAAdapter } from '@layr-labs/agentkit-eigenda';
import dotenv from 'dotenv';
import * as fs from 'fs';
dotenv.config();

export interface VerifiableResponse {
  content: string;
  proof: any;
}

export class Agent {
  private opacity: OpacityAdapter;
  private eigenDA: EigenDAAdapter;

  constructor() {
    // Initialize Opacity adapter for verifiable AI inference
    this.opacity = new OpacityAdapter({
      apiKey: process.env.OPENAI_KEY!,
      teamId: process.env.OPACITY_TEAM_ID!,
      teamName: process.env.OPACITY_TEAM_NAME!,
      opacityProverUrl: process.env.OPACITY_PROVER_URL!,
    });

    // Initialize EigenDA adapter for data availability logging
    this.eigenDA = new EigenDAAdapter({
      privateKey: process.env.EIGENDA_PRIVATE_KEY!,
      apiUrl: process.env.EIGENDA_API_URL!,
      rpcUrl: process.env.EIGENDA_BASE_RPC_URL!,
      creditsContractAddress: process.env.EIGENDA_CREDITS_CONTRACT!,
      flushInterval: 5000, // Flush logs every 5 seconds
      maxBufferSize: 100, // Maximum number of logs to buffer
    });
  }

  /**
   * Initialize all adapters
   */
  async initialize() {
    try {
      console.log('Initializing Opacity adapter...');
      await this.opacity.initialize();

      console.log('Initializing EigenDA adapter...');
      await this.eigenDA.initialize();

      console.log('All adapters initialized successfully');
    } catch (error) {
      console.error('Error initializing adapters:', error);
      throw error;
    }
  }

  /**
   * Generate verifiable text using Opacity and log to EigenDA
   */
  async generateVerifiableText(prompt: string): Promise<VerifiableResponse> {
    try {
      console.log('Generating text with prompt:', prompt);
      // Generate text with proof using Opacity
      const result = await this.opacity.generateText(prompt);

      console.log('Generated result:', result);
  
      // // Convert the result to an array of lines
      // let lines = result["content"].split("\n");
  
      // // Find the actual CSV data start and end indices
      // let startIndex = lines.findIndex(line => line.startsWith("news,date,website"));
      // let endIndex = lines.findIndex(line => line.toLowerCase().includes("this table is purely fictional"));
  
      // // Extract only the valid CSV lines
      // if (startIndex !== -1 && endIndex !== -1) {
      //     lines = lines.slice(startIndex, endIndex);
      // }
  
      // // Convert the cleaned lines back to a string
      // let cleanedContent = lines.join("\n");
  
      // // Define the file path
      // let filePath = "/Users/hanxu/Desktop/TreeHack/TreeHack2025/Output.csv";
  
      // // Save the cleaned CSV data
      // fs.writeFile(filePath, cleanedContent, (err) => {
      //     if (err) throw err;
      // });
      
      // Log the generation to EigenDA
      await this.eigenDA.info('Text Generation', {
        prompt,
        result: result.content,
        hasProof: !!result.proof,
      });

      return result;
    } catch (error) {
      console.error('Error in generateVerifiableText:', error);
      await this.eigenDA.error('Text Generation Failed', { prompt, error });
      throw error;
    }
  }

  /**
   * Utility method to log information directly to EigenDA
   */
  async logInfo(message: string, metadata: any): Promise<void> {
    await this.eigenDA.info(message, metadata);
  }
}

// Export a factory function to create new agent instances
export const createAgent = async (): Promise<Agent> => {
  const agent = new Agent();
  await agent.initialize();
  return agent;
}; 