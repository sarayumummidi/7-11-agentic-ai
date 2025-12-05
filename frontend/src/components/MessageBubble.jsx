import React from 'react'

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

  return (
    <div style={wrapperStyle}>
      {label && <span style={labelStyle}>{label}</span>}
      <div style={bubbleStyle}>{text}</div>
    </div>
  )
}

export default MessageBubble
