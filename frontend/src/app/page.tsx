"use client";

import { useState, useRef, useEffect } from "react";

interface Message {
  role: "user" | "bot";
  content: string;
  userQuery?: string; // Store the original user query for feedback
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    { role: "bot", content: "Chào bạn! Tôi là trợ lý tra cứu phụ tùng xe máy. Bạn cần tìm phụ tùng gì hay có câu hỏi gì không?" }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [showFeedbackModal, setShowFeedbackModal] = useState(false);
  const [selectedMessage, setSelectedMessage] = useState<Message | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleFeedbackClick = (message: Message) => {
    setSelectedMessage(message);
    setShowFeedbackModal(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMsg = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMsg }]);
    setIsLoading(true);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userMsg }),
      });

      if (!response.ok) {
        throw new Error("Lấy dữ liệu thất bại");
      }

      const data = await response.json();
      setMessages((prev) => [...prev, { role: "bot", content: data.reply, userQuery: userMsg }]);
    } catch (error: any) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", content: "Xin lỗi, đã có lỗi kết nối đến máy chủ AI: " + error.message }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-gray-50 dark:bg-gray-900">
      <div className="w-full max-w-3xl bg-white dark:bg-gray-800 rounded-2xl shadow-xl overflow-hidden flex flex-col h-[85vh]">
        {/* Header */}
        <div className="bg-blue-600 p-4 text-white flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center font-bold text-blue-600 text-xl shadow-inner">
              AI
            </div>
            <div>
              <h1 className="font-bold text-lg">Trợ Lý Phụ Tùng</h1>
              <p className="text-blue-100 text-xs text-opacity-80">Tra cứu nhanh hơn, tư vấn chuẩn hơn</p>
            </div>
          </div>
        </div>

        {/* Chat window */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50 dark:bg-gray-900">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div className={`max-w-[75%] ${msg.role === "user" ? "" : "w-full"}`}>
                <div
                  className={`rounded-2xl p-4 shadow-sm ${
                    msg.role === "user"
                      ? "bg-blue-600 text-white rounded-br-none"
                      : "bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-100 border border-gray-100 dark:border-gray-700 rounded-bl-none"
                  }`}
                >
                  <div
                    className="prose prose-sm dark:prose-invert prose-p:leading-relaxed"
                    dangerouslySetInnerHTML={{ __html: msg.content.replace(/\n/g, "<br/>").replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>") }}
                  />
                </div>
                {/* Feedback button for bot messages (except the first welcome message) */}
                {msg.role === "bot" && index > 0 && msg.userQuery && (
                  <button
                    onClick={() => handleFeedbackClick(msg)}
                    className="mt-2 text-xs text-gray-500 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-400 flex items-center gap-1 transition-colors"
                  >
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                    Góp ý / Cập nhật
                  </button>
                )}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 text-gray-800 dark:text-gray-100 rounded-2xl p-4 rounded-bl-none shadow-sm flex items-center space-x-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }}></div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input area */}
        <div className="p-4 bg-white dark:bg-gray-800 border-t border-gray-100 dark:border-gray-700">
          <form onSubmit={handleSubmit} className="flex space-x-2 relative">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Hỏi về mã sản phẩm, giá, cách lắp ráp..."
              className="flex-1 border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white rounded-full px-6 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm transition-all"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="bg-blue-600 hover:bg-blue-700 text-white rounded-full px-6 py-3 font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm flex items-center justify-center"
            >
              Gửi lên
            </button>
          </form>
        </div>
      </div>

      {/* Feedback Modal */}
      {showFeedbackModal && selectedMessage && (
        <FeedbackModal
          message={selectedMessage}
          onClose={() => {
            setShowFeedbackModal(false);
            setSelectedMessage(null);
          }}
        />
      )}
    </main>
  );
}

// Feedback Modal Component
function FeedbackModal({ message, onClose }: { message: Message; onClose: () => void }) {
  const [correctedKnowledge, setCorrectedKnowledge] = useState("");
  const [submittedBy, setSubmittedBy] = useState("Staff");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!correctedKnowledge.trim() || isSubmitting) return;

    setIsSubmitting(true);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/knowledge/feedback`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_query: message.userQuery || "",
          ai_response: message.content,
          corrected_knowledge: correctedKnowledge,
          submitted_by: submittedBy,
        }),
      });

      if (!response.ok) {
        throw new Error("Gửi góp ý thất bại");
      }

      setSubmitSuccess(true);
      setTimeout(() => {
        onClose();
      }, 2000);
    } catch (error: any) {
      alert("Lỗi khi gửi góp ý: " + error.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-blue-600 text-white p-4 rounded-t-2xl flex items-center justify-between">
          <h2 className="text-xl font-bold">Góp ý / Cập nhật kiến thức</h2>
          <button
            onClick={onClose}
            className="text-white hover:bg-blue-700 rounded-full p-1 transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {submitSuccess ? (
          <div className="p-8 text-center">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
              Gửi thành công!
            </h3>
            <p className="text-gray-600 dark:text-gray-300">
              Góp ý của bạn đã được gửi đến quản lý để xem xét.
            </p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="p-6 space-y-4">
            {/* Original Query */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Câu hỏi gốc:
              </label>
              <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-3 text-sm text-gray-800 dark:text-gray-200">
                {message.userQuery}
              </div>
            </div>

            {/* AI Response */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Câu trả lời của AI:
              </label>
              <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-3 text-sm text-gray-800 dark:text-gray-200 max-h-32 overflow-y-auto">
                <div dangerouslySetInnerHTML={{ __html: message.content.replace(/\n/g, "<br/>").replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>") }} />
              </div>
            </div>

            {/* Corrected Knowledge */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Thông tin chính xác <span className="text-red-500">*</span>
              </label>
              <textarea
                value={correctedKnowledge}
                onChange={(e) => setCorrectedKnowledge(e.target.value)}
                placeholder="Nhập thông tin chính xác hoặc bổ sung kiến thức mới..."
                className="w-full border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[120px]"
                required
              />
            </div>

            {/* Submitted By */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Người gửi:
              </label>
              <input
                type="text"
                value={submittedBy}
                onChange={(e) => setSubmittedBy(e.target.value)}
                className="w-full border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Tên nhân viên"
              />
            </div>

            {/* Actions */}
            <div className="flex gap-3 pt-4">
              <button
                type="button"
                onClick={onClose}
                className="flex-1 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-white rounded-lg px-6 py-3 font-medium transition-colors"
                disabled={isSubmitting}
              >
                Hủy
              </button>
              <button
                type="submit"
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-6 py-3 font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                disabled={!correctedKnowledge.trim() || isSubmitting}
              >
                {isSubmitting ? "Đang gửi..." : "Gửi góp ý"}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
