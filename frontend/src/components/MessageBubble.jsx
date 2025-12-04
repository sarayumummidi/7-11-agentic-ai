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
    padding: '18px 26px',
    borderRadius: '24px',
    fontSize: '16px',
    maxWidth: '70%',
    lineHeight: '1.5',
    backgroundColor: isUser ? 'rgba(255, 255, 255, 0.95)' : 'rgba(255, 255, 255, 0.25)',
    border: isUser ? '1px solid rgba(0, 0, 0, 0.05)' : '1px solid rgba(255, 255, 255, 0.3)',
    boxShadow: isUser
      ? '0 4px 20px rgba(0, 0, 0, 0.08), 0 1px 3px rgba(0, 0, 0, 0.05)'
      : '0 8px 32px rgba(0, 0, 0, 0.12), inset 0 1px 0 rgba(255, 255, 255, 0.4)',
    color: '#333',
    backdropFilter: isUser ? 'none' : 'blur(20px) saturate(180%)',
    WebkitBackdropFilter: isUser ? 'none' : 'blur(20px) saturate(180%)',
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
