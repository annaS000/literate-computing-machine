import * as React from "react";
import { useState } from "react";

const App: React.FC = () => {
  const [token, setToken] = useState<string | null>(null);

  const openLoginDialog = () => {
    const loginUrl = "https://localhost:5000/login";

    Office.context.ui.displayDialogAsync(
      loginUrl,
      { height: 50, width: 50, displayInIframe: true },
      (asyncResult) => {
        if (asyncResult.status === Office.AsyncResultStatus.Failed) {
          console.error("Failed to open dialog:", asyncResult.error.message);
          return;
        }

        const dialog: Office.Dialog = asyncResult.value;  // Ensure typing

        console.log("Dialog opened successfully.");

        dialog.addEventHandler(Office.EventType.DialogMessageReceived, (arg: Office.DialogParentMessageReceivedEventArgs) => {
          console.log("Message received from dialog:", arg.message);  // Log the received message
          
          // Process the message and store the token
          processMessage(arg.message);
          dialog.close();  // Close the dialog after receiving the message
        });

        dialog.addEventHandler(Office.EventType.DialogEventReceived, () => {
          console.log("Dialog closed by user or system.");
        });
      }
    );
  };

  const processMessage = (message: string) => {
    Office.context.roamingSettings.set("authToken", message);
    Office.context.roamingSettings.saveAsync(() => {
      console.log("Token saved to roaming settings.");
    });
    setToken(message);
    console.log("Token set in state:", message);
  };

  return (
    <div>
      {token ? (
        <div>Token received: {token}</div>
      ) : (
        <button onClick={openLoginDialog}>Login with Flask OAuth</button>
      )}
    </div>
  );
};

export default App;
