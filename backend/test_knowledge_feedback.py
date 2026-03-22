"""
Integration tests for Knowledge Feedback Loop API endpoints
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_test_result(test_name, success, message=""):
    """Print test result in a formatted way"""
    status = "[PASS]" if success else "[FAIL]"
    print(f"{status} {test_name}")
    if message:
        print(f"      {message}")

def test_submit_feedback():
    """Test POST /api/knowledge/feedback"""
    print("\n=== Testing: Submit Feedback ===")

    payload = {
        "user_query": "Gia phanh truoc xe SH 2023 la bao nhieu?",
        "ai_response": "Gia phanh truoc SH 2023 la 450,000 VND",
        "corrected_knowledge": "Gia phanh truoc SH 2023 la 520,000 VND. Phanh truoc chinh hang Honda, ma SKU: SH23-BRK-FR, bao hanh 12 thang.",
        "submitted_by": "Test Staff"
    }

    try:
        response = requests.post(f"{BASE_URL}/api/knowledge/feedback", json=payload)

        if response.status_code == 200:
            data = response.json()
            if data.get("success") and "feedback_id" in data:
                print_test_result("Submit Feedback", True, f"Feedback ID: {data['feedback_id']}")
                return data["feedback_id"]
            else:
                print_test_result("Submit Feedback", False, "Invalid response format")
                return None
        else:
            print_test_result("Submit Feedback", False, f"Status code: {response.status_code}")
            return None
    except Exception as e:
        print_test_result("Submit Feedback", False, str(e))
        return None

def test_get_pending_feedbacks():
    """Test GET /api/admin/knowledge/pending"""
    print("\n=== Testing: Get Pending Feedbacks ===")

    try:
        response = requests.get(f"{BASE_URL}/api/admin/knowledge/pending?status=pending")

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print_test_result("Get Pending Feedbacks", True, f"Found {len(data)} pending feedbacks")
                if len(data) > 0:
                    print(f"      Sample: ID={data[0]['id']}, Status={data[0]['status']}")
                return True
            else:
                print_test_result("Get Pending Feedbacks", False, "Invalid response format")
                return False
        else:
            print_test_result("Get Pending Feedbacks", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        print_test_result("Get Pending Feedbacks", False, str(e))
        return False

def test_approve_feedback(feedback_id):
    """Test POST /api/admin/knowledge/{id}/approve"""
    print("\n=== Testing: Approve Feedback ===")

    if not feedback_id:
        print_test_result("Approve Feedback", False, "No feedback ID provided")
        return False

    payload = {
        "reviewed_by": "Test Manager",
        "notes": "Integration test approval"
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/admin/knowledge/{feedback_id}/approve",
            json=payload
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_test_result("Approve Feedback", True, f"Approved feedback #{feedback_id}")
                return True
            else:
                print_test_result("Approve Feedback", False, "Invalid response format")
                return False
        else:
            print_test_result("Approve Feedback", False, f"Status code: {response.status_code}")
            print(f"      Response: {response.text}")
            return False
    except Exception as e:
        print_test_result("Approve Feedback", False, str(e))
        return False

def test_reject_feedback(feedback_id):
    """Test POST /api/admin/knowledge/{id}/reject"""
    print("\n=== Testing: Reject Feedback ===")

    if not feedback_id:
        print_test_result("Reject Feedback", False, "No feedback ID provided")
        return False

    payload = {
        "reviewed_by": "Test Manager",
        "notes": "Integration test rejection"
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/admin/knowledge/{feedback_id}/reject",
            json=payload
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_test_result("Reject Feedback", True, f"Rejected feedback #{feedback_id}")
                return True
            else:
                print_test_result("Reject Feedback", False, "Invalid response format")
                return False
        else:
            print_test_result("Reject Feedback", False, f"Status code: {response.status_code}")
            print(f"      Response: {response.text}")
            return False
    except Exception as e:
        print_test_result("Reject Feedback", False, str(e))
        return False

def test_get_approved_feedbacks():
    """Test getting approved feedbacks"""
    print("\n=== Testing: Get Approved Feedbacks ===")

    try:
        response = requests.get(f"{BASE_URL}/api/admin/knowledge/pending?status=approved")

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print_test_result("Get Approved Feedbacks", True, f"Found {len(data)} approved feedbacks")
                return True
            else:
                print_test_result("Get Approved Feedbacks", False, "Invalid response format")
                return False
        else:
            print_test_result("Get Approved Feedbacks", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        print_test_result("Get Approved Feedbacks", False, str(e))
        return False

def test_get_rejected_feedbacks():
    """Test getting rejected feedbacks"""
    print("\n=== Testing: Get Rejected Feedbacks ===")

    try:
        response = requests.get(f"{BASE_URL}/api/admin/knowledge/pending?status=rejected")

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print_test_result("Get Rejected Feedbacks", True, f"Found {len(data)} rejected feedbacks")
                return True
            else:
                print_test_result("Get Rejected Feedbacks", False, "Invalid response format")
                return False
        else:
            print_test_result("Get Rejected Feedbacks", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        print_test_result("Get Rejected Feedbacks", False, str(e))
        return False

def run_all_tests():
    """Run all integration tests"""
    print("=" * 60)
    print("KNOWLEDGE FEEDBACK LOOP - INTEGRATION TESTS")
    print("=" * 60)
    print("\nMake sure the backend server is running at http://localhost:8000")
    print("\nStarting tests in 3 seconds...")
    time.sleep(3)

    # Test 1: Submit feedback (for approval)
    feedback_id_for_approval = test_submit_feedback()

    # Small delay
    time.sleep(1)

    # Test 2: Submit another feedback (for rejection)
    print("\n=== Testing: Submit Second Feedback (for rejection test) ===")
    payload_reject = {
        "user_query": "Test query for rejection",
        "ai_response": "Test AI response",
        "corrected_knowledge": "This will be rejected",
        "submitted_by": "Test Staff 2"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/knowledge/feedback", json=payload_reject)
        if response.status_code == 200:
            feedback_id_for_rejection = response.json().get("feedback_id")
            print_test_result("Submit Second Feedback", True, f"Feedback ID: {feedback_id_for_rejection}")
        else:
            feedback_id_for_rejection = None
            print_test_result("Submit Second Feedback", False, f"Status code: {response.status_code}")
    except Exception as e:
        feedback_id_for_rejection = None
        print_test_result("Submit Second Feedback", False, str(e))

    time.sleep(1)

    # Test 3: Get pending feedbacks
    test_get_pending_feedbacks()

    time.sleep(1)

    # Test 4: Approve feedback
    test_approve_feedback(feedback_id_for_approval)

    time.sleep(1)

    # Test 5: Reject feedback
    test_reject_feedback(feedback_id_for_rejection)

    time.sleep(1)

    # Test 6: Get approved feedbacks
    test_get_approved_feedbacks()

    time.sleep(1)

    # Test 7: Get rejected feedbacks
    test_get_rejected_feedbacks()

    print("\n" + "=" * 60)
    print("TESTS COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()
