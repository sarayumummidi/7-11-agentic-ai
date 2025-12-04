import React, { useState, useRef, useEffect } from 'react'
import ChatInput from '../components/ChatInput'
import MessageBubble from '../components/MessageBubble'
import logo from '../assets/7-11logo.png'

const ChatPage = () => {
  const [messages, setMessages] = useState([
    { id: 1, text: 'What can I ask you to do?', isUser: true },
    {
      id: 2,
      text: 'You can ask me about our slushie flavors, store locations, or current rewards!',
      isUser: false,
    },
  ])

  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = (text) => {
    // Add User Message
    const userMessage = { id: Date.now(), text, isUser: true }
    setMessages((prev) => [...prev, userMessage])

    // Simulate AI Response (Placeholder until your backend is connected)
    setTimeout(() => {
      const aiMessage = {
        id: Date.now() + 1,
        text: "I'm checking on that for you...",
        isUser: false,
      }
      setMessages((prev) => [...prev, aiMessage])
    }, 1000)
  }

  const styles = {
    // --- LAYOUT ---
    container: {
      height: '100vh',
      width: '100vw',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      fontFamily:
        'Manrope, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
      position: 'relative',
      overflow: 'hidden',
      backgroundColor: 'transparent',
    },
    gradientBackground: {
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      width: '100%',
      height: '100%',
      backgroundColor: 'rgba(255, 255, 255, 0.5)',
      background:
        'radial-gradient(circle at 42% 80%, #f2b0b0 0px, transparent 40%), radial-gradient(circle at 62% 81%, #ffc085 0px, transparent 40%),rgb(255, 255, 255)',
      backgroundRepeat: 'no-repeat',
      backgroundSize: 'cover',
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
      zIndex: 1,
    },
    titleContainer: {
      fontSize: '32px',
      fontWeight: '900',
      paddingBottom: '0px',
      letterSpacing: '-0.5px',
      color: '#333',
      textShadow: '0 2px 10px rgba(255,255,255,0.5)',
    },
    stripeBar: {
      paddingTop: '0px',
      display: 'flex',
      width: '80px',
      height: '8px',
      borderRadius: '4px',
      overflow: 'hidden',
      boxShadow: '0 2px 5px rgba(0,0,0,0.1)',
    },
    stripeOrange: { flex: 1, backgroundColor: '#F58220' },
    stripeGreen: { flex: 1, backgroundColor: '#008060' },
    stripeRed: { flex: 1, backgroundColor: '#EE1C25' },
    logo: {
      height: '42px',
      marginLeft: '8px',
      paddingBottom: '4px',
      display: 'inline-block',
      verticalAlign: 'middle',
    },

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
      borderRadius: '10px',
      fontSize: '16px',
      maxWidth: '70%',
      lineHeight: '1.5',
      // User = White with subtle shadow, AI = Glassmorphism
      backgroundColor: isUser
        ? 'rgba(246, 245, 245, 0.56)'
        : 'rgba(155, 155, 155, 0.08)',
      border: isUser
        ? '1px solid rgba(224, 221, 221, 0.83)'
        : '1px solid rgba(255, 255, 255, 0.86)',
      boxShadow: isUser
        ? '0 4px 20px rgba(0, 0, 0, 0.08), 0 1px 3px rgba(0, 0, 0, 0.05)'
        : '0 8px 32px rgba(0, 0, 0, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.4)',
      color: '#333',
      backdropFilter: isUser ? 'none' : 'blur(20px) saturate(180%)',
      WebkitBackdropFilter: isUser ? 'none' : 'blur(20px) saturate(180%)',
      // Add a little "tail" visual direction
      borderBottomRightRadius: isUser ? '4px' : '24px',
      borderBottomLeftRadius: isUser ? '24px' : '4px',
      transition: 'all 0.3s ease',
    }),

    // --- INPUT AREA ---
    floatingInputContainer: {
      width: '90%',
      maxWidth: '800px',
      marginBottom: '30px',
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      backdropFilter: 'blur(20px) saturate(180%)',
      WebkitBackdropFilter: 'blur(20px) saturate(180%)',
      border: '1px solid rgba(175, 175, 175, 0.63)',
      borderRadius: '10px',
      boxShadow:
        '0 10px 40px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.5)',
      overflow: 'hidden',
      zIndex: 2,
    },
  }

  return (
    <div style={styles.container}>
      <div style={styles.gradientBackground} />

      <header style={styles.header}>
        <div style={styles.titleContainer} className="tangerine-regular">
          <span style={{ fontWeight: 700 }}>ask</span>
          <img src={logo} alt="7-11 logo" style={styles.logo} />
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
            <div style={styles.bubble(msg.isUser)}>{msg.text}</div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div style={styles.floatingInputContainer}>
        <ChatInput onSend={handleSendMessage} />
      </div>
    </div>
  )
}

export default ChatPage
