import { BrowserRouter, Routes, Route } from 'react-router-dom'
import ChatPage from './pages/ChatPage'
import ChatInput from './components/ChatInput'
import MessageBubble from './components/MessageBubble'
import SendButton from './components/SendButton'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ChatPage />} />
        <Route path="/chat-input" element={<ChatInput />} />
        <Route path="/message-bubble" element={<MessageBubble />} />
        <Route path="/send-button" element={<SendButton />} />
        <Route path="*" element={<p>Not found</p>} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
