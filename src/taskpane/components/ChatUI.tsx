import * as React from "react";
import { useState } from "react";

interface ChatUIProps {
  token: string;
}

const ChatUI: React.FC<ChatUIProps> = ({ token }) => {
  const [messages, setMessages] = useState<Array<{ text: string; sender: "user" | "ai" }>>([]);
  const [prompt, setPrompt] = useState("");
  const [selectedText, setSelectedText] = useState("");

  // Function to send message to the backend
  const sendMessage = async () => {
    // Ensure a token exists
    if (!token) {
      console.error("No authentication token found.");
      return;
    }

    if (!selectedText) {
      console.error("No text selected.");
      return;
    }

    try {
      const response = await fetch("https://localhost:5000/chat", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`, // Use the token passed as a prop
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: prompt,
          selected_text: selectedText,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error:", errorData.message || "Something went wrong");
        return;
      }

      const data = await response.json();

      // Add AI's response to the chat
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: prompt, sender: "user" },
        { text: data.response, sender: "ai" },
      ]);

      setPrompt(""); // Reset the input field
    } catch (error) {
      console.error("Error:", error);
    }
  };

  // Function to get selected text from the Word document
  const getSelectedText = async () => {
    try {
      await Word.run(async (context) => {
        const selection = context.document.getSelection();
        selection.load("text");
        await context.sync();

        if (selection.text) {
          setSelectedText(selection.text); // Set the selected text
        } else {
          console.error("No text selected in the document.");
        }
      });
    } catch (error) {
      console.error("Error getting selected text:", error);
    }
  };

  return (
    <div>
      <div className="chat-container">
        {messages.map((message, index) => (
          <div key={index} className={`chat-message ${message.sender}`}>
            <p>{message.text}</p>
          </div>
        ))}
      </div>
      <button onClick={getSelectedText}>Get Selected Text</button>
      <textarea
        placeholder="Write your prompt here..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
};

export default ChatUI;
