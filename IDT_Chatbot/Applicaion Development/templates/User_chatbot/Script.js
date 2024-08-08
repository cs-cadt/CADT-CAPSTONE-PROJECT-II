document.addEventListener('DOMContentLoaded', () => {
    const chatbotSpeedBubble = document.querySelector('.chatbot-speedbuble');
    const chatbot = document.querySelector('.chatbot');
    const closeBtn = document.querySelector('.small-img');
    const chatbox = document.querySelector('.chatbox');
    const chatInput = document.querySelector(".chat-input textarea");
    const sendChatBtn = document.querySelector("#send-btn");
    const img = document.querySelector('.small-img-top '); // Modified this line to target the image inside .small-img-top
    const containerChatbot = document.querySelector('.container-chatbot');
    const cancelButton = document.querySelector('.cancel-Button');
    const yesButton = document.querySelector('.yes-Button');

    let userMessage;
    const API_KEY = "^2yv7bhrvkrac$3k+qqaex*wcb2s#jwjkw7+&9f1&c@yxlk$ag";
    const inputInHeight = chatInput.scrollHeight;

    // Function to set a cookie
    const setCookie = (name, value, days) => {
        let expires = "";
        if (days) {
            const date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "") + expires + "; path=/";
    };

    // Function to get a cookie by name
    const getCookie = (name) => {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) == ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) == 0) {
                const cookieValue = c.substring(nameEQ.length, c.length);
                return cookieValue;
            }
        }
        return null;
    };

    // Function to load chat history from the cookie
    const loadChatHistory = () => {
        const chatHistory = getCookie("chatHistory");
        if (chatHistory) {
            const messages = JSON.parse(chatHistory);
            messages.forEach(message => {
                const chatLi = createChatLi(message.text, message.className,save=false);
                chatbox.appendChild(chatLi);
            });
            chatbox.scrollTo(0, chatbox.scrollHeight);
        }
    };

    // Function to store chat message in the cookie
    const storeChatMessage = (message, className) => {
        let chatHistory = getCookie("chatHistory");
        try {
            chatHistory = chatHistory ? JSON.parse(chatHistory) : [];
        } catch (error) {
            chatHistory = [];
        }
        chatHistory.push({ text: message, className: className });
        setCookie("chatHistory", JSON.stringify(chatHistory), 60);
    };

    const createChatLi = (message, className,save=true) => {
        const chatLi = document.createElement("li");
        chatLi.classList.add("chat", className);

        let avatarSrc = className === "outgoing" ? "images/question_logo_.png" : "images/response_logo.png";
        let imgClass = className === "outgoing" ? "nested-img" : "avatar";
        let chatContent = `<img src="${avatarSrc}" alt="Avatar" class="${imgClass}"> <p>${message}</p>`;
        chatLi.innerHTML = chatContent;

        // Store the chat message in the cookie
        if(save){
            storeChatMessage(message, className);
        }
        return chatLi;
    };
    
    async function fetchData(API_URL, requestOptions, messageElement) {
        try {
            const response = await fetch(API_URL, requestOptions);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const data = await response.json();
            console.log("Response data:", data.answer);
            if (data.answer) {
                const responseMessage = data.answer.trim();
                messageElement.textContent = responseMessage;
                createChatLi(responseMessage, "incoming");
            } else {
                throw new Error("Empty response from API");
            }
        } catch (error) {
            const errorMessage = error.message.replace(/\s+/g, '-');
            messageElement.classList.add("error", errorMessage);
            console.error("Error:", error);
        } finally {
            chatbox.scrollTo(0, chatbox.scrollHeight);
        }
        return true;
    }

    const generateResponse = async(chatElement) => {
        const API_URL = "http://127.0.0.1:8000/api/response/";
        const messageElement = chatElement.querySelector("p");

        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `${API_KEY}`,
                "Accept": "application/json"
            },
            body: JSON.stringify({
                "question": chatInput.value
            })
        };
        await fetchData(API_URL, requestOptions, messageElement);
    };
    
    const handleChat = async() => {
        userMessage = chatInput.value.trim();
        if (!userMessage) return;
        chatInput.style.height = `40px`;
        const outgoingChatLi = createChatLi(userMessage, "outgoing");
        chatbox.appendChild(outgoingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
        const incomingChatLi = createChatLi("Thinking...", "incoming",save=false);
        chatbox.appendChild(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
        setTimeout(async () => {
            await generateResponse(incomingChatLi);
        }, 200);
        chatInput.value = "";
    };

    chatInput.addEventListener("input", () => {
        chatInput.style.height = `${inputInHeight}px`;
        chatInput.style.height = `${chatInput.scrollHeight}px`;
    });

    chatInput.addEventListener("keydown", async(e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            await handleChat();
        }
    });

    sendChatBtn.addEventListener("click", handleChat);

    // Function to toggle chatbot visibility
    const toggleChatbot = () => {
        chatbot.classList.toggle('show');
    };

    // Event listener for clicking the chat bubble
    chatbotSpeedBubble.addEventListener('click', toggleChatbot);

    // Event listener for clicking the close button
    closeBtn.addEventListener('click', () => {
        chatbot.classList.remove('show');
    });

    // Event listener for clicking outside the chatbot
    document.addEventListener('click', (e) => {
        if (!chatbot.contains(e.target) && !chatbotSpeedBubble.contains(e.target)) {
            // Click occurred outside the chatbot and its speed bubble
            chatbot.classList.remove('show');
        }
    });

    // Function to toggle visibility of recommendation buttons
    const toggleRecommendationButtons = () => {
        const buttonsContainer = document.querySelector('.buttons');

        if (chatbox.scrollTop === chatbox.scrollHeight - chatbox.clientHeight) {
            buttonsContainer.style.display = 'none';
        } else {
            buttonsContainer.style.display = 'flex';
        }
    };

    // Event listener for scrolling in chatbox
    chatbox.addEventListener('scroll', toggleRecommendationButtons);

    // Show confirmation box when the image is clicked
    img.addEventListener('click', () => {
        containerChatbot.style.display = 'flex';
    });
    
    // Hide confirmation box when cancel button is clicked
    cancelButton.addEventListener('click', () => {
        containerChatbot.style.display = 'none';
    });

    // Clear chatbox and start new chat when yes button is clicked
    yesButton.addEventListener('click', () => {
        const cookies = document.cookie.split(";");

        // Loop through all cookies and delete each one
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i];
            const eqPos = cookie.indexOf("=");
            const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
            // Set the cookie's expiration date to the past
            document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
        }
        // Clear all messages in chatbox
        chatbox.innerHTML = '';

        // Create a new incoming chat message
        const newIncomingMessage = createChatLi("Hello, I’m a chatbot of CADT.", "incoming",save=false);
        chatbox.appendChild(newIncomingMessage);

        // Optionally add an image or any other element to the chatbox
        const incomingImage = document.createElement("img");

        chatbox.appendChild(incomingImage);

        // Scroll to the bottom of the chatbox
        chatbox.scrollTo(0, chatbox.scrollHeight);
        // Hide the confirmation box
        containerChatbot.style.display = 'none';
    });

    // Load chat history when the page is loaded
    loadChatHistory();
});
