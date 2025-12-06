import React, { useState, useRef, useEffect } from 'react'
import ChatInput from '../components/ChatInput'
import MessageBubble from '../components/MessageBubble'
import logo from '../assets/7-11logo.png'

const ChatPage = () => {
  const [messages, setMessages] = useState([
    {
      id: 2,
      text: 'Ask me anything about 7-11!',
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

  const handleSendMessage = async (text) => {
    // Add User Message
    const userMessage = { id: Date.now(), text, isUser: true }
    setMessages((prev) => [...prev, userMessage])

    // Create placeholder AI message that will be updated as stream arrives
    const aiMessageId = Date.now() + 1
    const aiMessage = {
      id: aiMessageId,
      text: '',
      isUser: false,
    }
    setMessages((prev) => [...prev, aiMessage])

    // Connect to WebSocket and stream response
    try {
      // Determine WebSocket URL based on environment
      // Default to localhost:8000 for development
      const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const apiUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
      const wsHost = apiUrl
        .replace(/^https?:\/\//, '')
        .replace(/^wss?:\/\//, '')
      const wsUrl = `${wsProtocol}//${wsHost}/stream`

      const ws = new WebSocket(wsUrl)

      ws.onopen = () => {
        // Send the question to the backend
        ws.send(JSON.stringify({ question: text }))
      }

      ws.onmessage = (event) => {
        // Update the AI message with streaming text
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === aiMessageId
              ? {
                  ...msg,
                  // Replace "Thinking..." with the actual response when streaming starts
                  text:
                    msg.text === 'Thinking...'
                      ? event.data
                      : msg.text + event.data,
                }
              : msg
          )
        )
      }

      ws.onerror = (error) => {
        console.error('WebSocket error:', error)
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === aiMessageId
              ? {
                  ...msg,
                  text: 'Sorry, there was an error connecting to the server.',
                }
              : msg
          )
        )
      }

      ws.onclose = () => {
        console.log('WebSocket connection closed')
      }
    } catch (error) {
      console.error('Error setting up WebSocket:', error)
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === aiMessageId
            ? {
                ...msg,
                text: 'Sorry, there was an error connecting to the server.',
              }
            : msg
        )
      )
    }
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
      overflowX: 'hidden',
      padding: '20px',
      display: 'flex',
      flexDirection: 'column',
      gap: '24px',
      zIndex: 1,
      scrollbarWidth: 'none',
      msOverflowStyle: 'none',
      position: 'relative',
    },

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
          <MessageBubble
            key={msg.id}
            text={msg.text}
            isUser={msg.isUser}
            label={msg.isUser ? 'ME' : 'OUR AI'}
          />
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
