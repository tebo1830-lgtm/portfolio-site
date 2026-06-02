require("dotenv").config();  // Loads your .env file

const twilio = require("twilio");

// Create Twilio client using your credentials
const client = twilio(
  process.env.TWILIO_ACCOUNT_SID,
  process.env.TWILIO_AUTH_TOKEN
);

// Function to send message
async function sendMessage() {
  try {
    const message = await client.messages.create({
      body: "Hello Sifiso! Your WhatsApp API is working ✅",
      from: process.env.TWILIO_WHATSAPP_NUMBER,
      to: process.env.MY_WHATSAPP_NUMBER
    });

    console.log("✅ Message sent successfully!");
    console.log("Message SID:", message.sid);

  } catch (error) {
    console.error("❌ Error sending message:");
    console.error(error.message);
  }
}

// Run the function
sendMessage();