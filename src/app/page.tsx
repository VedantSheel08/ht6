'use client';
import React from "react";

// Add type declarations for Web Speech API
declare global {
  interface Window {
    SpeechRecognition: any;
    webkitSpeechRecognition: any;
  }
}

interface SpeechRecognitionEvent {
  results: {
    [index: number]: {
      [index: number]: {
        transcript: string;
      };
    };
  };
}

interface SpeechRecognitionErrorEvent {
  error: string;
}

export default function Home() {
  const [input, setInput] = React.useState("");
  const [isTyping, setIsTyping] = React.useState(false);
  const [isListening, setIsListening] = React.useState(false);
  const [speechSupported, setSpeechSupported] = React.useState(false);
  
  React.useEffect(() => {
    setSpeechSupported('webkitSpeechRecognition' in window || 'SpeechRecognition' in window);
  }, []);

  const handleSubmit = async () => {
    console.log("User input:", input);
    try {
      await fetch("/api/log-response", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ input }),
      });
    } catch (err) {
      console.error("Failed to log response:", err);
    }
    setInput("");
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSubmit();
    }
  };

  const startListening = () => {
    if (!speechSupported) return;
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';
    
    recognition.onstart = () => {
      setIsListening(true);
    };
    
    recognition.onresult = (event: SpeechRecognitionEvent) => {
      const transcript = event.results[0][0].transcript;
      setInput(transcript);
    };
    
    recognition.onerror = (event: SpeechRecognitionErrorEvent) => {
      console.error('Speech recognition error:', event.error);
      setIsListening(false);
    };
    
    recognition.onend = () => {
      setIsListening(false);
    };
    
    recognition.start();
  };

  return (
    <div
      style={{
        background: "linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0f0f0f 100%)",
        color: "#ffffff",
        fontFamily: "'Press Start 2P', cursive",
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "20px",
        position: "relative",
        overflow: "hidden",
      }}
    >
      <style>
        {`
          @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
          
          @keyframes gridPulse {
            0% { opacity: 0.15; }
            100% { opacity: 0.05; }
          }
          
          @keyframes inputPulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
          }
          
          @keyframes glitch {
            0% { transform: translate(0); }
            20% { transform: translate(-2px, 2px); }
            40% { transform: translate(-2px, -2px); }
            60% { transform: translate(2px, 2px); }
            80% { transform: translate(2px, -2px); }
            100% { transform: translate(0); }
          }
          
          @keyframes shimmer {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
          }
          
          @keyframes micPulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
          }
          
          @keyframes rainbow {
            0% { color: #ff0000; }
            14% { color: #ff7f00; }
            28% { color: #ffff00; }
            42% { color: #00ff00; }
            57% { color: #0000ff; }
            71% { color: #4b0082; }
            85% { color: #9400d3; }
            100% { color: #ff0000; }
          }
          
          .rainbow-text {
            animation: rainbow 3s linear infinite;
          }
        `}
      </style>

      {/* Animated background grid */}
      <div
        style={{
          content: '',
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          backgroundImage: 
            "linear-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 255, 255, 0.08) 1px, transparent 1px)",
          backgroundSize: "20px 20px",
          animation: "gridPulse 4s ease-in-out infinite alternate",
          zIndex: -1,
        }}
      />

      {/* Scanlines */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          background: "linear-gradient(transparent 50%, rgba(255, 255, 255, 0.02) 50%)",
          backgroundSize: "100% 4px",
          pointerEvents: "none",
          zIndex: 2,
        }}
      />

      <div
        style={{
          textAlign: "center",
          maxWidth: "800px",
          zIndex: 1,
          width: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        {/* ASCII Goose Art */}
        <pre
          style={{
            fontSize: "clamp(0.15rem, 0.5vw, 0.25rem)",
            lineHeight: "1",
            color: "rgba(255, 255, 255, 0.8)",
            marginBottom: "2rem",
            fontFamily: "monospace",
            whiteSpace: "pre",
            overflow: "visible",
          }}
        >
{`                                                                                                                                                                                                               
                                                                                                                                                                                                               
                                                                                                                                                                                                               
                                                                                                                                                                                                               
                                                                                            =--::.::-=                                                                                                         
                                                                                        -:::::::::-==-..-                                                                                                      
                                                                                    =---++**++-::.-+=::=:.-                                                                                                    
                                                                                =----==  +***#++++::==+=::..                                                                                                   
                                                                             +=-=+:-+ +++*=+++==+ :.   ++=:..                                                                                                  
                                                                           +--+ :-= =+=*+-=  ==   ...    +*-..                                                                                                 
                                                                          =-+ =:=+++=+ =--  ==+   -..      =-:..                                               -=                                              
                                                                        =-+  -:+++++* =:=   -=     ..      +--:..                                             -:-+=*                                           
                                                                      +-=*  --*++++* =:=   ==      :.       =-=:..                                            =:-*##=                                          
                                                                     =-+   --++=++  =:=   *-+      :.:      =-==:..                                           =--##*-                                          
                                                                    ==+   --++==+  +:=    ==       -..      +--+:.                                            +-:*@**                                          
                                                                   ==*  +=-====*  +-=    +-=        :.      +-:--:..                                          =--+%+:..                                        
                                                                  ==* +--:++=+%  %=-     +-         =..     +--+-:.                                           =-+*%%+==+-=                                     
                                                                 +-*+=*#-= ==%   +-*     ==          ..    #*==*=-:.                                          =:+*@%+=+--*@                                    
                                                                 ==+#@ =:+*+#   +-=     +-+          ..   %%+=- +=:.:                                         =:=#@%+=%@@%@                                    
                                                                 =+@@  -- +*+   ==      +-           ..  ###+++ -=-..                                         =-+%@%+=%@%%@                                    
                                                                #*=   +-+ +*+  ==*      =-           -.  ##*+=* :==:                                         *#-*#%%++*%                                       
                                                               %@%-=  =-**#*+ +:=       -=           :.- ##*+-  .+== .                                       #%=+#%*=                                          
                                                             %%@@ +-= --#*#*+ =-       +:=            .. ##*+- -:+=+.-*****#%%*+=##%#%%%%@@@@@%@@%%%%        #%*+*#*+                                          
                                                            %@@@    =-=-###++*:=       +.+            ..#**++=*=-*-+.=*****+#@@@@@@@@@@@@@@@@@@@@@@@@@%%%%@@@@%++*#                                            
                                                           %@@@@@@@@@@@@@@@@@@%#       =.#   ********+:=***++=*-=*-+:=****+#@@@@@@@@@@@@@@@@@@@@@@%%%%%#%@++.:=---                                             
                                                         %@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%%#@@%@-..::::                                             
                                                       %@%% @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%##@##@-...:-:                                             
                                                     %%@%   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%#@@%@@#-..:.:::                                            
                                                   #%@%%    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@######%@#%#:..... .                                            
                                                 ##%@@@@####%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@######%@#%#:.....                                              
                                                #%@@@@@%-::=*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@###**@@#@%#-:...    .                                          
                                              *#%@@@@@@@=--=+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##***@#@%%@%*-.      .                                         
                                            ###*=#%@@@@@*+*++%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%******%%#@##*- . .    .                                        
                                          ###... %@@@@@@@@%#%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%***++@%#@#@#*-                                                 
                                        #%%#  ..:*@@@@@#+++**%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#***+*@%@#@%***:                                                
                                      #%%**  %%#:.*#%@%++===-*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#*****#@%@#***+=:.. .                                           
                                     %%##   @@@@%%**+++++*=+*#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*******%%@*++++=...... . . +                                    
                                     ##*    =====+=*=+##*+++**@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#*******#*++=%+=-:-::-.... .                                    
                                      #*++++--:::::::::::=+*==@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@**######**++---====-=--=:=-.                                    
                                  ..-++=-:.......::......:-=+*++#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*****##%%##+-:-+====+==+==-+                                    
                            ......:=-.........................#%%*++#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@******#######+++++**+++++                                       
                         ....       :....:-....::...................-##*==+*##%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#*****###**+==+++**+                                            
                        .::         ::........:..................:::-=+++++++++**********##++*%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#####*=-====#%****##=#                                          
                       :-         -==-==:::-==-::::.................:-=+++++==++++++++++===---=++++==-:-+++***##%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@#*==--:::=#@@##%##%%*#                                          
                       -:     =+++*++++%%%%%##++++*******==----::::::--===++=======-====---:::---===-:::-======================+++**###*+++++==---:::.:.::=%@@@@%**%%*                                         
                    ++++++***#*##*****####%@@%#++=*+**+==========+*#*######*++==----=-::::...:::::::....:::::::::::::::----::::::::::-======--:::::.::-=##*-::+%@@#*@%                                         
                 **#*#####*******%%#*######%%@@@@%%@%%@@%#%%%%###**#*##*##*#*******+##+---:::::::::....................::::...........-----::::::::+#@@%%@@@@@@@@@@@%+*                                        
               ##%%%%%%%####***##***#%#*%##*%#@@@@%@@@@@@@@@@@@@@@@@%#*++++*#*######+++++++++#+*++==-=----::..........................:::::::-=*@%*=::*%@@@@@@@@@@@@@#%#=                                      
             *#%%%%%%##%%%%###*#####%@@%*%%###%%@@@%@@@@@@@@#%@@@@@@@@@@@@@@@@@@@@@%#%%%%#**+++*++*++*+****=---::-:::::::::............::-#%%*+=+*#%@@@@@@%%@@@@@@%##%**@%++                                   
             %%%%*+======+*%%##**####*##@%%@#%@%@@@%@@@@@@@@%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%#*+-:::--==+++++*+==+=---==***=-=%%@@@@@@@@@@@@@@@%%%#%%%@@@@@%=#%*   @*=                                 
            %%%#+==+**+=++==*%%##%*%%#%%@@##%%@%%%@%@@@@@@@@%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@%@@@@@@@@@@@@@@@@@@%@@@@%@@@@@@@@@@%@@%%@@%@@%%%%%%%%%%%%%@@@@%*=**    @#+                               
           %%%#==++*++=--=**==#%##%%%#%%@@%#%@%%%%%#@@@@@@@@@%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%#%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@@@@@@@@%%##%#%#%%%%@@@@@@@@@@@@*%*=+     @#=                             
           %%%+==+++**----+**+=+%#####%#*%%@%@@#%#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%##**###*++++*%*%##@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%%%%@@@@@@@@@@@@@*%#+=      @*-                           
          #%%*==++++**----=++=+=+%%###%@%%@@@#%@@@@%#%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%*+++++**+++***#*##+******#@@@@@@@@@@@@@@@@%%@@@@@@@@@@@%%%%%%%%%@@@@@@@@@@@@@@@@@##*+=*      @+=                         
          %%%+-====**+-----=++*+=+%#%@@%%%@@@%%@@@@@@%%%      @@@@@@@@@@@@@@@@@@##*+#*+*++++***++**%#*###%*%#**#*%*@@@@@@@@@@@@@*%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%*%*=+       %-                        
          %%%=-==-:::--===-::----=*%##%@####@@%@@%@@@##%           @@@@@@@@@@#+###%%*#%###%##%*+++%*+***#%#**##**###%%@@@@@@@@@@*%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%@%%@%%@*=*       @-=                      
          %%#=--=-----====--------=%%%@@%%@@@@@%@@@%@%%%                  %*#%#%@@%%%%%%%%%%%%%%%#+*++***#%%%*#*#*#*%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%%+=::-#%%@@@+=        @-                      
          #%#=--==-----=---------==*%%%%%@@@@@@@%%@@@@%%                 *#%@@%@@%%%%%%%@%%%%%%%#%%#%#=#%+**+*%%#*%#+#*@#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@#+=--::..:+%@#+=#        -=                     
           %#+---===------=----=+*==%%%%#%@%%@@@%@@@@@@                 %%@@@@%@@%%*+==++#%@%%%%%%%%##*+%%++#*#%@%+*%@@%%##@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@@#==-:::....:.#%#++%       +-                     
           %%*-:---=+-::--=---=++*+-%%%%%%@@@@@%@@@@@@@                #%@@@@@%+=------------=#%%%%@@%%#*+%*#*%%%@@**#@%%#@#@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@*++====-+*#@@#**@%++%#      *:                     
           #%#=::---+-::::-----=+**-#%%%%@@@@@@@@@@@@@@               #%@@@@%=---==++++++===----=#%%%@@@%%%@#+%#**%@**#%#*@%#@@@@@@@@@@@@@@@@@@@@@@@@@@%%%*++=--====#@@@@@@@@@=*%%%     +-                     
            ##*-:::----:..:::-:-+++-#%%@@@@@@@@@@@@@@@               %%@@@@*---=++++####=---=+*=---*%@@@%@##*%++##*#@@##@##+@#%%%%%%%%%%%@@@@@@@@@@@@@@%%%*+++--===#@@@@@@@@@%=##*=     :-                     
            ###+:::::----------:-=--#@@@@@@@@@@@@@@@@@               %@@@@+--=++++*####*-::--=**##=--#@@@@@%%%@#**%#%%@%*%%@##**++****#####%@@@@@@@@@@##%#+***++++@@@@@@@@@@@*+%%*:     -*                     
             ##*=::::----=+=----:--=%%@@@@@@@@@@@@@@@               @@@@@*---=+++*#####+----:-+*@@@#=-=%@@@%##**@@%#%##@%**#%%%%  .......:=*#%%%%%@@%#+*##*#**#%%%@@@@@@@@@@%+#@#-=    #=%                     
              ##*=:.::--=++++=---:-+#%@@@@@@@@@@@@@@@               %@@@%---=+==****###=------=*@@@@*==-*%@%%#%#*@%##%%%#%%*%#%#..        .::-++%@@@%@%%%**%*######@@@@@@@@@+*@*:=    #:*                      
               ##*+::.:----=+++=--=%%%@@@@@@@@@@@@@@                %@@@*---=-:-=+++++*---:----#@@@@**+=-+%%%%#%#**%#***@%%@@**+#=:..      ..:----=*#%%%#####****##%@@@@@@@*+@*+     #-#                       
                ###*-::.:::::--:-=#%%@@@@@@@@@@@@@                  %@@%=---=--:::::---------::+%#*****+=-+%%%@#%#*+#@%%%**#%@%*#*#*=-:.. ........:::.....-=#####%%#   @@@#+%@     #+*%                        
                  ###*=:::::::--+%%%%@@@@@@@@@@@                    @@@%---==------::---==++=-::-++******===%%%@%@@#+#%@%@#*#%%@##**+++==:............  ....#%#++*%++    +=+   #*+#@                           
                   %####*+===*#%%%%@@@@@@@@@@                       @@@%----==---:----=========-::-=+++***==+%@%%%%#%#%%@%@@##@%@#*=+=---:==:.......    ...::*@@%%@@@@@%%%%%@@@%@                              
                     @%#%%%%%%%%@@@@@@@@@@                          @@@%----=-=+------====-----=--::::::---==*%@@%%@@@%%%%@@%##%%@#*+====-========... ......:+%%%@@@   *++                                     
                         @@@@@@@@@@@@                                @@%=-:----+*=--------------=----------===%%@@%#*#%%*##@@@@%#*%-:==-:-=---====:..........=%%##%  #++*                                      
                                                                     %%%*-:----=**+-:-----++-----=---------===+%@@%@%#*#@%@%*#@@@%#=--==--=======-:::.......:=%@@#%*+++                                        
                                                                     %%%%-::----++++-::::--===---=--------=*+==%@@@%@@@#*%@@@#%%%@@+====--+++=====-:::::::.=-#%%@#+++                                          
                                                                      %%%+-::---=+++-::::-------==----=*@@@@%==*@@@@@@%@@@@%@@#@@@#+++====+=+=====-::::::::::#*++**                                            
                                                                      %%%%-::::--===--:::::---===---=@@@@@@@@==+@@@@@@%@@@@@@@%@@%%%#*=--=+-======--:::---::+*#                                                
                                                                       %%%#-::::-------:::::::::----=#@@@@@@@===%@@@@@%#%@%%@@@@%%%     *+**%#+=-::-:::-----                                                   
                                                                        %%#+-:::::-------::::::::----++#@@@@%===%@@@@@@@#@@@%@@@@@                =-----=-                                                     
                                                                        %%%%+::::::-------==--------:=++*#@@+-==%@@@@@@@%%@@%@%@@%                                                                             
                                                                         @%%%+::.::-----+*****=------:===+*#--=+@@@@@@@@@@@@@@@@@                                                                              
                                                                           %@%#:::::--==+******+-----:-====---=#@@@@@@@@@@@@@@@@                                                                               
                                                                            @@%#-::.::--:-=+****+=------=----=+@@@@@@@%%@@@@@@@                                                                                
                                                                             @@%%*:::.::::-:--==++=-----:----=#@@@@@@@@@@@@@@                                                                                  
                                                                              @@%%%+:::::::::------=-----:--=#@@@@@@@%%@@@@@                                                                                   
                                                                                %@%%%+-:::::::::::----::---+%@@@@@@@@@@@@@                                                                                     
                                                                                 %@@@%%#=-:::::::::::----+#@@@@@@@@@@@@@                                                                                       
                                                                                   @@%@@@%#*=---------+#%@%@@@@@@@@@@@                                                                                         
                                                                                     @@@@@@@@@%%%%%%%%%%@@@@@@@@@@@@                                                                                           
                                                                                        @@@@@@@@@@@@@@@@@@@@@@@@@@                                                                                             `}
        </pre>
        
        <h1
          style={{
            fontSize: "clamp(2rem, 6vw, 4rem)",
            marginBottom: "1rem",
            textShadow: "none",
            animation: "rainbow 3s linear infinite",
            letterSpacing: "0.2em",
            cursor: "pointer",
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.animation = "glitch 0.3s, rainbow 3s linear infinite";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.animation = "rainbow 3s linear infinite";
          }}
        >
          intellidrive
        </h1>
        
        <p
          style={{
            fontSize: "clamp(0.6rem, 2vw, 1rem)",
            marginBottom: "3rem",
            color: "rgba(255, 255, 255, 0.7)",
            letterSpacing: "0.1em",
            lineHeight: "1.8",
          }}
        >
          Your LLM on wheels.
        </p>
        
        <div style={{ 
          marginBottom: "2rem", 
          position: "relative", 
          display: "flex", 
          alignItems: "center", 
          gap: "15px", 
          justifyContent: "center",
          width: "100%",
          maxWidth: "600px"
        }}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask intellidrive anything"
            style={{
              background: "rgba(255, 255, 255, 0.05)",
              backdropFilter: "blur(10px)",
              border: "1px solid rgba(255, 255, 255, 0.2)",
              color: "#ffffff",
              fontFamily: "'Press Start 2P', cursive",
              fontSize: "clamp(0.5rem, 1.5vw, 0.8rem)",
              padding: "15px 20px",
              width: "100%",
              maxWidth: "600px",
              borderRadius: "8px",
              outline: "none",
              textAlign: "center",
              letterSpacing: "0.05em",
              transition: "all 0.3s ease",
              boxShadow: 
                "inset 0 0 20px rgba(255, 255, 255, 0.1), 0 8px 32px rgba(0, 0, 0, 0.3)",
            }}
            onFocus={(e) => {
              e.target.style.borderColor = "rgba(255, 255, 255, 0.4)";
              e.target.style.background = "rgba(255, 255, 255, 0.1)";
              e.target.style.boxShadow =
                "inset 0 0 20px rgba(255, 255, 255, 0.2), 0 8px 32px rgba(255, 255, 255, 0.1)";
              e.target.style.animation = "inputPulse 1.5s ease-in-out infinite";
            }}
            onBlur={(e) => {
              e.target.style.borderColor = "rgba(255, 255, 255, 0.2)";
              e.target.style.background = "rgba(255, 255, 255, 0.05)";
              e.target.style.boxShadow =
                "inset 0 0 20px rgba(255, 255, 255, 0.1), 0 8px 32px rgba(0, 0, 0, 0.3)";
              e.target.style.animation = "";
            }}
          />
          
          {speechSupported && (
            <button
              onClick={startListening}
              disabled={isListening}
              style={{
                background: isListening 
                  ? "linear-gradient(135deg, rgba(255, 100, 100, 0.2), rgba(255, 50, 50, 0.1))"
                  : "linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05))",
                backdropFilter: "blur(10px)",
                border: isListening 
                  ? "1px solid rgba(255, 100, 100, 0.5)" 
                  : "1px solid rgba(255, 255, 255, 0.3)",
                color: "#ffffff",
                padding: "15px",
                cursor: isListening ? "not-allowed" : "pointer",
                borderRadius: "8px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                minWidth: "50px",
                minHeight: "50px",
                transition: "all 0.3s ease",
                animation: isListening ? "micPulse 1s ease-in-out infinite" : "none",
                boxShadow: 
                  "0 8px 32px rgba(0, 0, 0, 0.3), inset 0 0 20px rgba(255, 255, 255, 0.1)",
              }}
              onMouseEnter={(e) => {
                if (!isListening) {
                  e.currentTarget.style.background = "linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1))";
                  e.currentTarget.style.borderColor = "rgba(255, 255, 255, 0.5)";
                  e.currentTarget.style.transform = "translateY(-2px)";
                }
              }}
              onMouseLeave={(e) => {
                if (!isListening) {
                  e.currentTarget.style.background = "linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05))";
                  e.currentTarget.style.borderColor = "rgba(255, 255, 255, 0.3)";
                  e.currentTarget.style.transform = "";
                }
              }}
              title={isListening ? "Listening..." : "Click to speak"}
            >
              <svg 
                width="20" 
                height="20" 
                viewBox="0 0 24 24" 
                fill="none" 
                stroke="currentColor" 
                strokeWidth="2" 
                strokeLinecap="round" 
                strokeLinejoin="round"
              >
                <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/>
                <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
                <line x1="12" y1="19" x2="12" y2="23"/>
                <line x1="8" y1="23" x2="16" y2="23"/>
              </svg>
            </button>
          )}
        </div>
        
        <button
          onClick={handleSubmit}
          style={{
            background: "linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05))",
            backdropFilter: "blur(10px)",
            border: "1px solid rgba(255, 255, 255, 0.3)",
            color: "#ffffff",
            fontFamily: "'Press Start 2P', cursive",
            fontSize: "clamp(0.6rem, 1.8vw, 1rem)",
            padding: "18px 40px",
            cursor: "pointer",
            transition: "all 0.3s ease",
            textTransform: "uppercase",
            letterSpacing: "0.1em",
            position: "relative",
            overflow: "hidden",
            borderRadius: "8px",
            boxShadow: 
              "0 8px 32px rgba(0, 0, 0, 0.3), inset 0 0 20px rgba(255, 255, 255, 0.1)",
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = "linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1))";
            e.currentTarget.style.borderColor = "rgba(255, 255, 255, 0.5)";
            e.currentTarget.style.transform = "translateY(-2px)";
            e.currentTarget.style.boxShadow = 
              "0 12px 40px rgba(255, 255, 255, 0.1), inset 0 0 20px rgba(255, 255, 255, 0.2)";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = "linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05))";
            e.currentTarget.style.borderColor = "rgba(255, 255, 255, 0.3)";
            e.currentTarget.style.transform = "";
            e.currentTarget.style.boxShadow = 
              "0 8px 32px rgba(0, 0, 0, 0.3), inset 0 0 20px rgba(255, 255, 255, 0.1)";
          }}
          onMouseDown={(e) => {
            e.currentTarget.style.transform = "scale(0.98)";
          }}
          onMouseUp={(e) => {
            e.currentTarget.style.transform = "translateY(-2px)";
          }}
        >
          Send it off~
        </button>
      </div>
    </div>
  );
}
