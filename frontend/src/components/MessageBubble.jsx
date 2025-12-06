import React from 'react'
import ReactMarkdown from 'react-markdown'

const MessageBubble = ({ text = '', isUser = false, label }) => {
  const wrapperStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: isUser ? 'flex-end' : 'flex-start',
  }
  const labelStyle = {
    fontSize: '12px',
    fontWeight: 'bold',
    color: '#888',
    marginBottom: '6px',
    marginLeft: '12px',
    marginRight: '12px',
    textTransform: 'uppercase',
  }

  const bubbleStyle = {
    padding: '10px 14px',
    borderRadius: '10px',
    fontSize: '16px',
    maxWidth: '70%',
    lineHeight: '1.5',
    // User = White with subtle shadow, AI = Glassmorphism
    backgroundColor: isUser
      ? 'rgba(255, 255, 255, 0.49)'
      : 'rgba(0, 0, 0, 0.04)',
    border: isUser
      ? '1px solid rgba(224, 221, 221, 0.83)'
      : '1px solid rgba(255, 255, 255, 0.86)',
    color: '#333',
    backdropFilter: isUser ? 'none' : 'blur(20px) saturate(180%)',
    WebkitBackdropFilter: isUser ? 'none' : 'blur(20px) saturate(180%)',
    // Add a little "tail" visual direction
    borderBottomRightRadius: isUser ? '4px' : '24px',
    borderBottomLeftRadius: isUser ? '24px' : '4px',
    transition: 'all 0.3s ease',
  }

  // Markdown styles for AI messages
  const markdownStyle = {
    margin: 0,
    fontFamily: 'Manrope',
  }

  return (
    <div style={wrapperStyle}>
      {label && <span style={labelStyle}>{label}</span>}
      <div style={bubbleStyle}>
        {isUser ? (
          text
        ) : (
          <div style={markdownStyle}>
            <ReactMarkdown
              components={{
                // Style headings
                h1: ({ children }) => (
                  <h1
                    style={{
                      fontSize: '24px',
                      fontWeight: 'bold',
                      marginTop: '12px',
                      marginBottom: '8px',
                    }}
                  >
                    {children}
                  </h1>
                ),
                h2: ({ children }) => (
                  <h2
                    style={{
                      fontSize: '20px',
                      fontWeight: 'bold',
                      marginTop: '10px',
                      marginBottom: '6px',
                    }}
                  >
                    {children}
                  </h2>
                ),
                h3: ({ children }) => (
                  <h3
                    style={{
                      fontSize: '18px',
                      fontWeight: 'bold',
                      marginTop: '8px',
                      marginBottom: '6px',
                    }}
                  >
                    {children}
                  </h3>
                ),
                // Style lists
                ul: ({ children }) => (
                  <ul
                    style={{
                      marginLeft: '20px',
                      marginTop: '8px',
                      marginBottom: '8px',
                    }}
                  >
                    {children}
                  </ul>
                ),
                ol: ({ children }) => (
                  <ol
                    style={{
                      marginLeft: '20px',
                      marginTop: '8px',
                      marginBottom: '8px',
                    }}
                  >
                    {children}
                  </ol>
                ),
                li: ({ children }) => (
                  <li style={{ marginBottom: '4px' }}>{children}</li>
                ),
                // Style paragraphs
                p: ({ children }) => (
                  <p
                    style={{
                      marginTop: '8px',
                      marginBottom: '8px',
                      margin: '8px 0',
                    }}
                  >
                    {children}
                  </p>
                ),
                // Style bold and italic
                strong: ({ children }) => (
                  <strong style={{ fontWeight: 'bold' }}>{children}</strong>
                ),
                em: ({ children }) => (
                  <em style={{ fontStyle: 'italic' }}>{children}</em>
                ),
              }}
            >
              {text}
            </ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  )
}

export default MessageBubble
