import React, { useState, useRef, useEffect } from 'react';
import ChatInput from '../components/ChatInput';
import MessageBubble from '../components/MessageBubble';

const ChatPage = () => {
  const [messages, setMessages] = useState([
    { id: 1, text: "What can I ask you to do?", isUser: true },
    { id: 2, text: "You can ask me about our slushie flavors, store locations, or current rewards!", isUser: false }
  ]);
  
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = (text) => {
    // Add User Message
    const userMessage = { id: Date.now(), text, isUser: true };
    setMessages((prev) => [...prev, userMessage]);

    // Simulate AI Response (Placeholder until your backend is connected)
    setTimeout(() => {
      const aiMessage = { 
        id: Date.now() + 1, 
        text: "I'm checking on that for you...", 
        isUser: false 
      };
      setMessages((prev) => [...prev, aiMessage]);
    }, 1000);
  };

  const styles = {
    // --- LAYOUT ---
    container: {
      height: '100vh',
      width: '100vw',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      fontFamily: "sans-serif",
      position: 'relative',
      overflow: 'hidden',
    },
    gradientBackground: {
      position: 'absolute',
      top: 0, left: 0, right: 0, bottom: 0,
      backgroundColor: '#f8f9fa',
      background: `
        radial-gradient(circle at 20% 20%, rgba(0, 128, 96, 0.12), transparent 50%), 
        radial-gradient(circle at 80% 80%, rgba(245, 130, 32, 0.12), transparent 50%)
      `,
      zIndex: -1,
    },
    
    // --- HEADER ---
    header: {
      marginTop: '40px',
      marginBottom: '20px',
      textAlign: 'center',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: '10px',
      zIndex: 1,
    },
    titleContainer: {
      fontSize: '32px',
      fontWeight: '900',
      letterSpacing: '-0.5px',
      color: '#333',
      textShadow: '0 2px 10px rgba(255,255,255,0.5)',
    },
    textOrange: { color: '#F58220' },
    textGreen:  { color: '#008060' },
    
    stripeBar: {
      display: 'flex',
      width: '80px',
      height: '8px',
      borderRadius: '4px',
      overflow: 'hidden',
      boxShadow: '0 2px 5px rgba(0,0,0,0.1)',
    },
    stripeOrange: { flex: 1, backgroundColor: '#F58220' },
    stripeGreen:  { flex: 1, backgroundColor: '#008060' },
    stripeRed:    { flex: 1, backgroundColor: '#EE1C25' },

    // --- CHAT AREA ---
    chatArea: {
      flex: 1,
      width: '100%',
      maxWidth: '1000px',
      overflowY: 'auto',
      padding: '0 20px 20px 20px',
      display: 'flex',
      flexDirection: 'column',
      gap: '24px',
      zIndex: 1,
      scrollbarWidth: 'none', 
      msOverflowStyle: 'none',
    },

    // --- MESSAGE STYLES (UPDATED) ---
    messageWrapper: (isUser) => ({
      display: 'flex',
      flexDirection: 'column',
      // SWAPPED: User aligns flex-end (Right), AI aligns flex-start (Left)
      alignItems: isUser ? 'flex-end' : 'flex-start', 
    }),
    label: {
      fontSize: '12px',
      fontWeight: 'bold',
      color: '#888',
      marginBottom: '6px',
      marginLeft: '12px',
      marginRight: '12px',
      textTransform: 'uppercase',
    },
    bubble: (isUser) => ({
      padding: '18px 26px',
      borderRadius: '24px',
      fontSize: '16px',
      maxWidth: '70%',
      lineHeight: '1.5',
      // User = White, AI = Glassy
      backgroundColor: isUser ? '#ffffff' : 'rgba(255, 255, 255, 0.7)',
      border: isUser ? 'none' : '1px solid rgba(0, 128, 96, 0.1)', 
      boxShadow: '0 4px 15px rgba(0,0,0,0.05)',
      color: '#333',
      backdropFilter: 'blur(5px)',
      // Add a little "tail" visual direction
      borderBottomRightRadius: isUser ? '4px' : '24px',
      borderBottomLeftRadius: isUser ? '24px' : '4px',
    }),

    // --- INPUT AREA ---
    floatingInputContainer: {
      width: '90%',
      maxWidth: '800px',
      marginBottom: '30px',
      backgroundColor: 'white',
      borderRadius: '20px',
      boxShadow: '0 10px 30px rgba(0,0,0,0.08)',
      overflow: 'hidden',
      zIndex: 2,
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.gradientBackground} />
      
      <header style={styles.header}>
        <div style={styles.titleContainer}>
          Ask <span style={styles.textOrange}>7</span>-<span style={styles.textGreen}>ELEVEN</span> AI
        </div>
        <div style={styles.stripeBar}>
          <div style={styles.stripeOrange} />
          <div style={styles.stripeGreen} />
          <div style={styles.stripeRed} />
        </div>
      </header>

      <div style={styles.chatArea}>
        {messages.map((msg) => (
          <div key={msg.id} style={styles.messageWrapper(msg.isUser)}>
            <span style={styles.label}>{msg.isUser ? 'ME' : 'OUR AI'}</span>
            <div style={styles.bubble(msg.isUser)}>
              {msg.text}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div style={styles.floatingInputContainer}>
        <ChatInput onSend={handleSendMessage} />
      </div>
    </div>
  );
};

export default ChatPage;
