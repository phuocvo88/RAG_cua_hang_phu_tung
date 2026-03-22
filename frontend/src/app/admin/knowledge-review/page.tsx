"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

interface FeedbackItem {
  id: number;
  user_query: string;
  ai_response: string;
  corrected_knowledge: string;
  submitted_by: string;
  status: string;
  created_at: string;
  reviewed_by?: string;
  reviewed_at?: string;
  notes?: string;
}

export default function AdminKnowledgeReview() {
  const [feedbacks, setFeedbacks] = useState<FeedbackItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedFeedback, setSelectedFeedback] = useState<FeedbackItem | null>(null);
  const [showActionModal, setShowActionModal] = useState(false);
  const [actionType, setActionType] = useState<"approve" | "reject">("approve");
  const [reviewerName, setReviewerName] = useState("Manager");
  const [notes, setNotes] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [statusFilter, setStatusFilter] = useState("pending");

  const loadFeedbacks = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/api/admin/knowledge/pending?status=${statusFilter}`
      );
      if (!response.ok) {
        throw new Error("Không thể tải danh sách góp ý");
      }
      const data = await response.json();
      setFeedbacks(data);
    } catch (error: any) {
      alert("Lỗi khi tải dữ liệu: " + error.message);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadFeedbacks();
  }, [statusFilter]);

  const handleAction = async () => {
    if (!selectedFeedback || isSubmitting) return;

    setIsSubmitting(true);

    try {
      const endpoint =
        actionType === "approve"
          ? `http://localhost:8000/api/admin/knowledge/${selectedFeedback.id}/approve`
          : `http://localhost:8000/api/admin/knowledge/${selectedFeedback.id}/reject`;

      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          reviewed_by: reviewerName,
          notes: notes || undefined,
        }),
      });

      if (!response.ok) {
        throw new Error(`Không thể ${actionType === "approve" ? "phê duyệt" : "từ chối"}`);
      }

      alert(
        `Đã ${actionType === "approve" ? "phê duyệt" : "từ chối"} góp ý thành công!`
      );

      // Reload feedbacks
      await loadFeedbacks();

      // Close modal
      setShowActionModal(false);
      setSelectedFeedback(null);
      setNotes("");
    } catch (error: any) {
      alert("Lỗi: " + error.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const openActionModal = (feedback: FeedbackItem, type: "approve" | "reject") => {
    setSelectedFeedback(feedback);
    setActionType(type);
    setShowActionModal(true);
    setNotes("");
  };

  return (
    <main className="min-h-screen bg-gray-50 dark:bg-gray-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
              Quản lý Góp ý Kiến thức
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              Xem xét và phê duyệt các góp ý từ nhân viên
            </p>
          </div>
          <Link
            href="/"
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
          >
            ← Về trang chủ
          </Link>
        </div>

        {/* Status Filter */}
        <div className="mb-6 flex gap-2">
          <button
            onClick={() => setStatusFilter("pending")}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              statusFilter === "pending"
                ? "bg-blue-600 text-white"
                : "bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
            }`}
          >
            Chờ xử lý
          </button>
          <button
            onClick={() => setStatusFilter("approved")}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              statusFilter === "approved"
                ? "bg-green-600 text-white"
                : "bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
            }`}
          >
            Đã duyệt
          </button>
          <button
            onClick={() => setStatusFilter("rejected")}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              statusFilter === "rejected"
                ? "bg-red-600 text-white"
                : "bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
            }`}
          >
            Đã từ chối
          </button>
        </div>

        {/* Feedback List */}
        {isLoading ? (
          <div className="text-center py-12">
            <div className="inline-block w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
            <p className="mt-4 text-gray-600 dark:text-gray-400">Đang tải...</p>
          </div>
        ) : feedbacks.length === 0 ? (
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-12 text-center">
            <p className="text-gray-500 dark:text-gray-400 text-lg">
              Không có góp ý nào với trạng thái này
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {feedbacks.map((feedback) => (
              <div
                key={feedback.id}
                className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-100 dark:border-gray-700"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-sm font-medium text-gray-500 dark:text-gray-400">
                        #{feedback.id}
                      </span>
                      <span
                        className={`px-3 py-1 rounded-full text-xs font-medium ${
                          feedback.status === "pending"
                            ? "bg-yellow-100 text-yellow-800"
                            : feedback.status === "approved"
                            ? "bg-green-100 text-green-800"
                            : "bg-red-100 text-red-800"
                        }`}
                      >
                        {feedback.status === "pending"
                          ? "Chờ xử lý"
                          : feedback.status === "approved"
                          ? "Đã duyệt"
                          : "Đã từ chối"}
                      </span>
                      <span className="text-sm text-gray-500 dark:text-gray-400">
                        Gửi bởi: {feedback.submitted_by}
                      </span>
                      <span className="text-sm text-gray-500 dark:text-gray-400">
                        {new Date(feedback.created_at).toLocaleString("vi-VN")}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {/* User Query */}
                  <div>
                    <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                      Câu hỏi:
                    </h3>
                    <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-3 text-sm text-gray-800 dark:text-gray-200">
                      {feedback.user_query}
                    </div>
                  </div>

                  {/* AI Response */}
                  <div>
                    <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                      Câu trả lời AI:
                    </h3>
                    <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-3 text-sm text-gray-800 dark:text-gray-200 max-h-32 overflow-y-auto">
                      {feedback.ai_response}
                    </div>
                  </div>

                  {/* Corrected Knowledge */}
                  <div>
                    <h3 className="text-sm font-semibold text-green-700 dark:text-green-400 mb-2">
                      Thông tin chính xác:
                    </h3>
                    <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-3 text-sm text-gray-800 dark:text-gray-200 max-h-32 overflow-y-auto">
                      {feedback.corrected_knowledge}
                    </div>
                  </div>
                </div>

                {/* Review Info */}
                {feedback.reviewed_by && (
                  <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      <strong>Người xét duyệt:</strong> {feedback.reviewed_by} •{" "}
                      <strong>Thời gian:</strong>{" "}
                      {feedback.reviewed_at
                        ? new Date(feedback.reviewed_at).toLocaleString("vi-VN")
                        : "N/A"}
                    </p>
                    {feedback.notes && (
                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                        <strong>Ghi chú:</strong> {feedback.notes}
                      </p>
                    )}
                  </div>
                )}

                {/* Actions */}
                {feedback.status === "pending" && (
                  <div className="mt-4 flex gap-3">
                    <button
                      onClick={() => openActionModal(feedback, "approve")}
                      className="flex-1 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
                    >
                      ✓ Phê duyệt
                    </button>
                    <button
                      onClick={() => openActionModal(feedback, "reject")}
                      className="flex-1 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
                    >
                      ✗ Từ chối
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Action Modal */}
      {showActionModal && selectedFeedback && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl max-w-lg w-full">
            <div
              className={`p-4 rounded-t-2xl text-white ${
                actionType === "approve" ? "bg-green-600" : "bg-red-600"
              }`}
            >
              <h2 className="text-xl font-bold">
                {actionType === "approve" ? "Phê duyệt góp ý" : "Từ chối góp ý"}
              </h2>
            </div>

            <div className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Người xét duyệt:
                </label>
                <input
                  type="text"
                  value={reviewerName}
                  onChange={(e) => setReviewerName(e.target.value)}
                  className="w-full border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Tên người xét duyệt"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Ghi chú (tùy chọn):
                </label>
                <textarea
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  className="w-full border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[100px]"
                  placeholder="Nhập ghi chú nếu cần..."
                />
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  onClick={() => {
                    setShowActionModal(false);
                    setSelectedFeedback(null);
                    setNotes("");
                  }}
                  className="flex-1 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-white rounded-lg px-6 py-3 font-medium transition-colors"
                  disabled={isSubmitting}
                >
                  Hủy
                </button>
                <button
                  onClick={handleAction}
                  className={`flex-1 text-white rounded-lg px-6 py-3 font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${
                    actionType === "approve"
                      ? "bg-green-600 hover:bg-green-700"
                      : "bg-red-600 hover:bg-red-700"
                  }`}
                  disabled={!reviewerName.trim() || isSubmitting}
                >
                  {isSubmitting
                    ? "Đang xử lý..."
                    : actionType === "approve"
                    ? "Xác nhận phê duyệt"
                    : "Xác nhận từ chối"}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
