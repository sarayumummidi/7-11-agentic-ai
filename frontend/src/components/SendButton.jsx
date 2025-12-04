import React from 'react'
import { LuSendHorizontal } from 'react-icons/lu'

const SendButton = ({ disabled, onClick }) => {
  return (
    <button onClick={onClick} disabled={disabled} style={{ background: 'none', border: 'none', cursor: 'pointer' }}>
      <LuSendHorizontal size={25} color='rgba(84, 86, 84, 0.86)' display = 'flex' alignItems='center' justifyContent='center' />
    </button>
  )
}

export default SendButton
