require("dotenv").config(); // Load environment variables from .env file
const {
  GoogleGenerativeAI,
} = require("@google/generative-ai");

// Load API key and system configuration from environment variables
const apiKey = process.env.GEMINI_API_KEY;
const skyeconfig = process.env.SKYE_MODEL_CONFIG;

if (!apiKey || !systemInstruction) {
  console.error("Please ensure GEMINI_API_KEY and SKYE_MODEL_CONFIG are set in the .env file.");
  process.exit(1);
}

// Initialize the Generative AI client
const genAI = new GoogleGenerativeAI(apiKey);

// Configure the generation settings
const generationConfig = {
  temperature: 1,
  topP: 0.95,
  topK: 40,
  maxOutputTokens: 8192,
  responseMimeType: "text/plain",
};

// Start the main interaction loop
async function main() {
  try {
    // Get the model
    const model = genAI.getGenerativeModel({
      model: "gemini-1.5-flash",
      systemInstruction : skyeconfig,
    });

    // Initialize a chat session
    const chatSession = model.startChat({
      generationConfig,
      history: [],
    });

    console.log("Press 'exit' to stop the conversation. (This conversation will not be recorded)");

    const readline = require("readline").createInterface({
      input: process.stdin,
      output: process.stdout,
    });

    const promptUser = () => {
      readline.question("You: ", async (userInput) => {
        if (userInput.toLowerCase().includes("exit")) {
          console.log("Goodbye!");
          readline.close();
          return;
        }

        try {
          // Send the user input to the chat session and receive a response
          const result = await chatSession.sendMessage(userInput);
          console.log("Skye:", result.response.text());
        } catch (error) {
          console.error("Excuse me? I won't say that :p\n", error.message);
        }

        // Continue the interaction loop
        promptUser();
      });
    };

    promptUser();
  } catch (error) {
    console.error("Error initializing the chat session:", error.message);
  }
}

// Run the main function
main();
