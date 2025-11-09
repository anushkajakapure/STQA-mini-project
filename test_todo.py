import pytest
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Test results storage
test_results = []

def log_test_result(test_id, description, test_type, expected, actual, status, remarks=""):
    """Helper function to log test results"""
    test_results.append({
        'Test ID': test_id,
        'Description': description,
        'Type': test_type,
        'Expected Result': expected,
        'Actual Result': actual,
        'Status': status,
        'Remarks': remarks
    })

class TestTodoApplication:
    """Test suite for Todo List Application"""
    
    @pytest.fixture(autouse=True)
    def setup_method(self, driver):
        """Setup before each test"""
        self.driver = driver
        self.driver.get("http://localhost:5500/index.html")  # Update this path
        self.wait = WebDriverWait(self.driver, 10)
        # Clear localStorage before each test
        self.driver.execute_script("localStorage.clear();")
        self.driver.refresh()
        time.sleep(0.5)
    
    # ============ FUNCTIONAL TESTS ============
    
    def test_01_page_title(self):
        """TC-01: Verify page title is displayed correctly"""
        try:
            title = self.driver.find_element(By.ID, "app-title")
            actual = title.text
            expected = "My Todo List"
            status = "PASS" if actual == expected else "FAIL"
            
            log_test_result(
                "TC-01",
                "Verify page title displays 'My Todo List'",
                "Functional",
                expected,
                actual,
                status
            )
            assert actual == expected
        except Exception as e:
            log_test_result("TC-01", "Verify page title", "Functional", 
                          "My Todo List", str(e), "FAIL", str(e))
            pytest.fail(str(e))
    
    def test_02_add_single_task(self):
        """TC-02: Verify adding a single task"""
        try:
            input_field = self.driver.find_element(By.ID, "todo-input")
            add_button = self.driver.find_element(By.ID, "add-btn")
            
            task_text = "Buy groceries"
            input_field.send_keys(task_text)
            add_button.click()
            time.sleep(0.5)
            
            tasks = self.driver.find_elements(By.CLASS_NAME, "todo-item")
            actual = len(tasks)
            expected = 1
            status = "PASS" if actual == expected else "FAIL"
            
            log_test_result(
                "TC-02",
                "Add a single task and verify it appears in the list",
                "Functional",
                f"{expected} task displayed",
                f"{actual} task(s) displayed",
                status
            )
            assert actual == expected
        except Exception as e:
            log_test_result("TC-02", "Add single task", "Functional",
                          "1 task displayed", str(e), "FAIL", str(e))
            pytest.fail(str(e))
    
    def test_03_add_task_enter_key(self):
        """TC-03: Verify adding task using Enter key"""
        try:
            input_field = self.driver.find_element(By.ID, "todo-input")
            
            input_field.send_keys("Test task with Enter")
            input_field.send_keys(Keys.RETURN)
            time.sleep(0.5)
            
            tasks = self.driver.find_elements(By.CLASS_NAME, "todo-item")
            actual = len(tasks)
            expected = 1
            status = "PASS" if actual == expected else "FAIL"
            
            log_test_result(
                "TC-03",
                "Add task using Enter key",
                "Functional",
                f"{expected} task added",
                f"{actual} task(s) added",
                status
            )
            assert actual == expected
        except Exception as e:
            log_test_result("TC-03", "Add task with Enter", "Functional",
                          "1 task added", str(e), "FAIL", str(e))
            pytest.fail(str(e))
    
    def test_04_add_multiple_tasks(self):
        """TC-04: Verify adding multiple tasks"""
        try:
            input_field = self.driver.find_element(By.ID, "todo-input")
            add_button = self.driver.find_element(By.ID, "add-btn")
            
            tasks_to_add = ["Task 1", "Task 2", "Task 3"]
            for task in tasks_to_add:
                input_field.send_keys(task)
                add_button.click()
                time.sleep(0.3)
            
            tasks = self.driver.find_elements(By.CLASS_NAME, "todo-item")
            actual = len(tasks)
            expected = 3
            status = "PASS" if actual == expected else "FAIL"
            
            log_test_result(
                "TC-04",
                "Add multiple tasks (3 tasks)",
                "Functional",
                f"{expected} tasks displayed",
                f"{actual} tasks displayed",
                status
            )
            assert actual == expected
        except Exception as e:
            log_test_result("TC-04", "Add multiple tasks", "Functional",
                          "3 tasks displayed", str(e), "FAIL", str(e))
            pytest.fail(str(e))
    
    def test_05_empty_task_validation(self):
        """TC-05: Verify validation for empty task"""
        try:
            add_button = self.driver.find_element(By.ID, "add-btn")
            add_button.click()
            time.sleep(0.5)
            
            # Check for alert
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            
            expected = "Please enter a task!"
            status = "PASS" if alert_text == expected else "FAIL"
            
            log_test_result(
                "TC-05",
                "Verify validation message for empty task",
                "Validation",
                expected,
                alert_text,
                status
            )
            assert alert_text == expected
        except Exception as e:
            log_test_result("TC-05", "Empty task validation", "Validation",
                          "Alert displayed", str(e), "FAIL", str(e))
            pytest.fail(str(e))
    
    def test_06_mark_task_complete(self):
        """TC-06: Verify marking a task as complete"""
        try:
            # Add a task first
            input_field = self.driver.find_element(By.ID, "todo-input")
            input_field.send_keys("Complete this task")
            input_field.send_keys(Keys.RETURN)
            time.sleep(0.5)
            
            # Click checkbox
            checkbox = self.driver.find_element(By.CLASS_NAME, "todo-checkbox")
            checkbox.click()
            time.sleep(0.5)
            
            # Verify task has completed class
            task = self.driver.find_element(By.CLASS_NAME, "todo-item")
            has_completed_class = "completed" in task.get_attribute("class")
            
            expected = True
            actual = has_completed_class
            status = "PASS" if actual == expected else "FAIL"
            
            log_test_result(
                "TC-06",
                "Mark task as complete using checkbox",
                "Functional",
                "Task marked as completed",
                "Task marked as completed" if actual else "Task not completed",
                status
            )
            assert has_completed_class
        except Exception as e:
            log_test_result("TC-06", "Mark task complete", "Functional",
                          "Task completed", str(e), "FAIL", str(e))
            pytest.fail(str(e))
    
    def test_07_unmark_task_complete(self):
        """TC-07: Verify unmarking a completed task"""
        try:
            # Add and complete a task
            input_field = self.driver.find_element(By.ID, "todo-input")
            input_field.send_keys("Task to toggle")
            input_field.send_keys(Keys.RETURN)
            time.sleep(0.5)
            
            checkbox = self.driver.find_element(By.CLASS_NAME, "todo-checkbox")
            checkbox.click()
            time.sleep(0.3)
            checkbox.click()  # Uncheck
            time.sleep(0.5)
            
            # Verify task doesn't have completed class
            task = self.driver.find_element(By.CLASS_NAME, "todo-item")
            has_completed_class = "completed" in task.get_attribute("class")
            
            expected = False
            actual = has_completed_class
            status = "PASS" if actual == expected else "FAIL"
            
            log_test_result(
                "TC-07",
                "Unmark completed task",
                "Functional",
                "Task marked as active",
                "Task marked as active" if not actual else "Task still completed",
                status
            )
            assert not has_completed_class
        except Exception as e:
            log_test_result("TC-07", "Unmark task", "Functional",
                          "Task active", str(e), "FAIL", str(e))
            pytest.fail(str(e))
    
    def test_08_delete_task(self):
        """TC-08: Verify deleting a task"""
        try:
            # Add a task
            input_field = self.driver.find_element(By.ID, "todo-input")
            input_field.send_keys("Task to delete")
            input_field.send_keys(Keys.RETURN)
            time.sleep(0.5)
            
            # Delete the task
            delete_btn = self.driver.find_element(By.CLASS_NAME, "delete-btn")
            delete_btn.click()
            time.sleep(0.5)
            
            tasks = self.driver.find_elements(By.CLASS_NAME, "todo-item")
            actual = len(tasks)
            expected = 0
            status = "PASS" if actual == expected else "FAIL"
            
            log_test_result(
                "TC-08",
                "Delete a task using delete button",
                "Functional",
                f"{expected} tasks remaining",
                f"{actual} tasks remaining",
                status
            )
            assert actual == expected
        except Exception as e:
            log_test_result("TC-08", "Delete task", "Functional",
                          "Task deleted", str(e), "FAIL", str(e))
            pytest.fail(str(e))
    
    def test_09_filter_all_tasks(self):
        """TC-09: Verify 'All' filter shows all tasks"""
        try:
            # Add tasks
            input_field = self.driver.find_element(By.ID, "todo-input")
            add_button = self.driver.find_element(By.ID, "add-btn")
            
            input_field.send_keys("Active Task")
            add_button.click()
            time.sleep(0.3)
            
            input_field.send_keys("Completed Task")
            add_button.click()
            time.sleep(0.3)
            
            # Complete second task
            checkboxes = self.driver.find_elements(By.CLASS_NAME, "todo-checkbox")
            checkboxes[1].click()
            time.sleep(0.3)
            
            # Click All filter
            all_filter = self.driver.find_element(By.CSS_SELECTOR, "[data-filter='all']")
            all_filter.click()
            time.sleep(0.5)
            
            tasks = self.driver.find_elements(By.CLASS_NAME, "todo-item")
            actual = len(tasks)
            expected = 2
            status = "PASS" if actual == expected else "FAIL"
            
            log_test_result(
                "TC-09",
                "Filter: All - displays all tasks",
                "Functional",
                f"{expected} tasks shown",
                f"{actual} tasks shown",
                status
            )
            assert actual == expected
        except Exception as e:
            log_test_result("TC-09", "Filter All", "Functional",
                          "All tasks shown", str(e), "FAIL", str(e))
            pytest.fail(str(e))
    
    def test_10_filter_active_tasks(self):
        """TC-10: Verify 'Active' filter shows only active tasks"""
        try:
            # Add tasks
            input_field = self.driver.find_element(By.ID, "todo-input")
            add_button = self.driver.find_element(By.ID, "add-btn")
            
            input_field.send_keys("Active Task")
            add_button.click()
            time.sleep(0.3)
            
            input_field.send_keys("Completed Task")
            add_button.click()
            time.sleep(0.3)
            
            # Complete second task
            checkboxes = self.driver.find_elements(By.CLASS_NAME, "todo-checkbox")
            checkboxes[1].click()
            time.sleep(0.3)
            
            # Click Active filter
            active_filter = self.driver.find_element(By.CSS_SELECTOR, "[data-filter='active']")
            active_filter.click()
            time.sleep(0.5)
            
            tasks = self.driver.find_elements(By.CLASS_NAME, "todo-item")
            actual = len(tasks)
            expected = 1
            status = "PASS" if actual == expected else "FAIL"
            
            log_test_result(
                "TC-10",
                "Filter: Active - displays only active tasks",
                "Functional",
                f"{expected} active task shown",
                f"{actual} task(s) shown",
                status
            )
            assert actual == expected
        except Exception as e:
            log_test_result("TC-10", "Filter Active", "Functional",
                          "Only active tasks", str(e), "FAIL", str(e))
            pytest.fail(str(e))
    
    def test_11_filter_completed_tasks(self):
        """TC-11: Verify 'Completed' filter shows only completed tasks"""
        try:
            # Add tasks
            input_field = self.driver.find_element(By.ID, "todo-input")
            add_button = self.driver.find_element(By.ID, "add-btn")
            
            input_field.send_keys("Active Task")
            add_button.click()
            time.sleep(0.3)
            
            input_field.send_keys("Completed Task")
            add_button.click()
            time.sleep(0.3)
            
            # Complete second task
            checkboxes = self.driver.find_elements(By.CLASS_NAME, "todo-checkbox")
            checkboxes[1].click()
            time.sleep(0.3)
            
            # Click Completed filter
            completed_filter = self.driver.find_element(By.CSS_SELECTOR, "[data-filter='completed']")
            completed_filter.click()
            time.sleep(0.5)
            
            tasks = self.driver.find_elements(By.CLASS_NAME, "todo-item")
            actual = len(tasks)
            expected = 1
            status = "PASS" if actual == expected else "FAIL"
            
            log_test_result(
                "TC-11",
                "Filter: Completed - displays only completed tasks",
                "Functional",
                f"{expected} completed task shown",
                f"{actual} task(s) shown",
                status
            )
            assert actual == expected
        except Exception as e:
            log_test_result("TC-11", "Filter Completed", "Functional",
                          "Only completed tasks", str(e), "FAIL", str(e))
            pytest.fail(str(e))
    
    def test_12_clear_completed_tasks(self):
        """TC-12: Verify clearing completed tasks"""
        try:
            # Add tasks
            input_field = self.driver.find_element(By.ID, "todo-input")
            add_button = self.driver.find_element(By.ID, "add-btn")
            
            for i in range(3):
                input_field.send_keys(f"Task {i+1}")
                add_button.click()
                time.sleep(0.2)
            
            # Complete two tasks
            checkboxes = self.driver.find_elements(By.CLASS_NAME, "todo-checkbox")
            checkboxes[0].click()
            time.sleep(0.2)
            checkboxes[1].click()
            time.sleep(0.3)
            
            # Clear completed
            clear_btn = self.driver.find_element(By.ID, "clear-completed")
            clear_btn.click()
            time.sleep(0.3)
            
            # Accept confirmation
            alert = self.driver.switch_to.alert
            alert.accept()
            time.sleep(0.5)
            
            tasks = self.driver.find_elements(By.CLASS_NAME, "todo-item")
            actual = len(tasks)
            expected = 1
            status = "PASS" if actual == expected else "FAIL"
            
            log_test_result(
                "TC-12",
                "Clear all completed tasks",
                "Functional",
                f"{expected} task remaining",
                f"{actual} task(s) remaining",
                status
            )
            assert actual == expected
        except Exception as e:
            log_test_result("TC-12", "Clear completed", "Functional",
                          "Completed tasks cleared", str(e), "FAIL", str(e))
            pytest.fail(str(e))
    
    def test_13_task_counter_accuracy(self):
        """TC-13: Verify task counter shows correct counts"""
        try:
            # Add tasks
            input_field = self.driver.find_element(By.ID, "todo-input")
            add_button = self.driver.find_element(By.ID, "add-btn")
            
            input_field.send_keys("Task 1")
            add_button.click()
            time.sleep(0.2)
            
            input_field.send_keys("Task 2")
            add_button.click()
            time.sleep(0.3)
            
            # Complete one task
            checkbox = self.driver.find_element(By.CLASS_NAME, "todo-checkbox")
            checkbox.click()
            time.sleep(0.5)
            
            counter = self.driver.find_element(By.ID, "task-count")
            actual = counter.text
            expected = "1 active, 1 completed"
            status = "PASS" if actual == expected else "FAIL"
            
            log_test_result(
                "TC-13",
                "Verify task counter displays correct counts",
                "Functional",
                expected,
                actual,
                status
            )
            assert actual == expected
        except Exception as e:
            log_test_result("TC-13", "Task counter", "Functional",
                          "Correct count", str(e), "FAIL", str(e))
            pytest.fail(str(e))
    
    # ============ UI/UX TESTS ============
    
    def test_14_input_field_placeholder(self):
        """TC-14: Verify input field has placeholder text"""
        try:
            input_field = self.driver.find_element(By.ID, "todo-input")
            actual = input_field.get_attribute("placeholder")
            expected = "Enter a new task..."
            status = "PASS" if actual == expected else "FAIL"
            
            log_test_result(
                "TC-14",
                "Input field displays placeholder text",
                "UI/UX",
                expected,
                actual,
                status
            )
            assert actual == expected
        except Exception as e:
            log_test_result("TC-14", "Input placeholder", "UI/UX",
                          "Placeholder visible", str(e), "FAIL", str(e))
            pytest.fail(str(e))
    
    def test_15_input_clears_after_add(self):
        """TC-15: Verify input field clears after adding task"""
        try:
            input_field = self.driver.find_element(By.ID, "todo-input")
            add_button = self.driver.find_element(By.ID, "add-btn")
            
            input_field.send_keys("Test task")
            add_button.click()
            time.sleep(0.5)
            
            actual = input_field.get_attribute("value")
            expected = ""
            status = "PASS" if actual == expected else "FAIL"
            
            log_test_result(
                "TC-15",
                "Input field clears after adding task",
                "UI/UX",
                "Input field empty",
                f"Input value: '{actual}'",
                status
            )
            assert actual == expected
        except Exception as e:
            log_test_result("TC-15", "Input clears", "UI/UX",
                          "Field cleared", str(e), "FAIL", str(e))
            pytest.fail(str(e))
    
    # ============ REGRESSION TESTS ============
    
    def test_16_persistence_after_refresh(self):
        """TC-16: Verify tasks persist after page refresh (localStorage)"""
        try:
            # Add tasks
            input_field = self.driver.find_element(By.ID, "todo-input")
            input_field.send_keys("Persistent task")
            input_field.send_keys(Keys.RETURN)
            time.sleep(0.5)
            
            # Refresh page
            self.driver.refresh()
            time.sleep(1)
            
            tasks = self.driver.find_elements(By.CLASS_NAME, "todo-item")
            actual = len(tasks)
            expected = 1
            status = "PASS" if actual == expected else "FAIL"
            
            log_test_result(
                "TC-16",
                "Tasks persist after page refresh",
                "Regression",
                f"{expected} task persisted",
                f"{actual} task(s) found",
                status
            )
            assert actual == expected
        except Exception as e:
            log_test_result("TC-16", "Persistence test", "Regression",
                          "Task persisted", str(e), "FAIL", str(e))
            pytest.fail(str(e))
    
    def test_17_long_task_text(self):
        """TC-17: Verify handling of long task text"""
        try:
            input_field = self.driver.find_element(By.ID, "todo-input")
            long_text = "A" * 100  # 100 characters
            
            input_field.send_keys(long_text)
            input_field.send_keys(Keys.RETURN)
            time.sleep(0.5)
            
            task_text = self.driver.find_element(By.CLASS_NAME, "todo-text")
            actual = task_text.text
            status = "PASS" if len(actual) <= 100 else "FAIL"
            
            log_test_result(
                "TC-17",
                "Handle long task text (100 chars)",
                "Boundary",
                "Text displayed correctly",
                f"Text length: {len(actual)} chars",
                status
            )
            assert len(actual) <= 100
        except Exception as e:
            log_test_result("TC-17", "Long text", "Boundary",
                          "Text handled", str(e), "FAIL", str(e))
            pytest.fail(str(e))
    
    def test_18_special_characters(self):
        """TC-18: Verify handling of special characters in task"""
        try:
            input_field = self.driver.find_element(By.ID, "todo-input")
            special_text = "Task with <>&\"' special chars"
            
            input_field.send_keys(special_text)
            input_field.send_keys(Keys.RETURN)
            time.sleep(0.5)
            
            task_text = self.driver.find_element(By.CLASS_NAME, "todo-text")
            actual = task_text.text
            status = "PASS" if special_text in actual else "FAIL"
            
            log_test_result(
                "TC-18",
                "Handle special characters in task text",
                "Security",
                "Special chars escaped properly",
                f"Text displayed: {actual}",
                status
            )
            assert special_text in actual
        except Exception as e:
            log_test_result("TC-18", "Special characters", "Security",
                          "Chars escaped", str(e), "FAIL", str(e))
            pytest.fail(str(e))
    
    def test_19_empty_state_message(self):
        """TC-19: Verify empty state message appears when no tasks"""
        try:
            empty_msg = self.driver.find_element(By.ID, "empty-message")
            is_displayed = empty_msg.is_displayed()
            
            expected = True
            actual = is_displayed
            status = "PASS" if actual == expected else "FAIL"
            
            log_test_result(
                "TC-19",
                "Empty state message displays when no tasks",
                "UI/UX",
                "Empty message visible",
                "Empty message visible" if actual else "Message not visible",
                status
            )
            assert is_displayed
        except Exception as e:
            log_test_result("TC-19", "Empty state", "UI/UX",
                          "Message shown", str(e), "FAIL", str(e))
            pytest.fail(str(e))
    
    def test_20_rapid_task_addition(self):
        """TC-20: Verify rapid task addition works correctly"""
        try:
            input_field = self.driver.find_element(By.ID, "todo-input")
            
            # Rapidly add 5 tasks
            for i in range(5):
                input_field.send_keys(f"Rapid Task {i+1}")
                input_field.send_keys(Keys.RETURN)
                time.sleep(0.1)
            
            time.sleep(0.5)
            tasks = self.driver.find_elements(By.CLASS_NAME, "todo-item")
            actual = len(tasks)
            expected = 5
            status = "PASS" if actual == expected else "FAIL"
            
            log_test_result(
                "TC-20",
                "Rapid task addition (5 tasks quickly)",
                "Performance",
                f"{expected} tasks added",
                f"{actual} tasks added",
                status
            )
            assert actual == expected
        except Exception as e:
            log_test_result("TC-20", "Rapid addition", "Performance",
                          "5 tasks added", str(e), "FAIL", str(e))
            pytest.fail(str(e))


# Pytest hooks to save results
def pytest_sessionfinish(session, exitstatus):
    """Save test results to CSV after all tests complete"""
    if test_results:
        with open('test_results.csv', 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['Test ID', 'Description', 'Type', 'Expected Result', 
                         'Actual Result', 'Status', 'Remarks']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(test_results)
        print(f"\n✓ Test results saved to test_results.csv")
        print(f"Total tests: {len(test_results)}")
        passed = sum(1 for r in test_results if r['Status'] == 'PASS')
        failed = sum(1 for r in test_results if r['Status'] == 'FAIL')
        print(f"Passed: {passed}, Failed: {failed}")