"""
Python Mini HR - 개인용 HR 관리 프로그램
간단한 직원 정보 관리 시스템
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# 데이터 저장 파일
DATA_FILE = 'employees.json'

# 직원 데이터 로드
def load_employees():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# 직원 데이터 저장
def save_employees(employees):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(employees, f, ensure_ascii=False, indent=2)

# 메인 페이지 - 직원 목록
@app.route('/')
def index():
    employees = load_employees()
    return render_template('index.html', employees=employees)

# 직원 추가 페이지
@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        employees = load_employees()
        
        # 새 직원 ID 생성
        new_id = max([emp.get('id', 0) for emp in employees], default=0) + 1
        
        # 새 직원 정보 생성
        new_employee = {
            'id': new_id,
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'department': request.form.get('department'),
            'position': request.form.get('position'),
            'hire_date': request.form.get('hire_date'),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        employees.append(new_employee)
        save_employees(employees)
        
        flash('직원이 성공적으로 추가되었습니다.', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_employee.html')

# 직원 상세 정보
@app.route('/employee/<int:employee_id>')
def employee_detail(employee_id):
    employees = load_employees()
    employee = next((emp for emp in employees if emp['id'] == employee_id), None)
    
    if employee is None:
        flash('직원을 찾을 수 없습니다.', 'error')
        return redirect(url_for('index'))
    
    return render_template('employee_detail.html', employee=employee)

# 직원 수정
@app.route('/edit/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    employees = load_employees()
    employee = next((emp for emp in employees if emp['id'] == employee_id), None)
    
    if employee is None:
        flash('직원을 찾을 수 없습니다.', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        employee['name'] = request.form.get('name')
        employee['email'] = request.form.get('email')
        employee['phone'] = request.form.get('phone')
        employee['department'] = request.form.get('department')
        employee['position'] = request.form.get('position')
        employee['hire_date'] = request.form.get('hire_date')
        employee['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        save_employees(employees)
        flash('직원 정보가 수정되었습니다.', 'success')
        return redirect(url_for('employee_detail', employee_id=employee_id))
    
    return render_template('edit_employee.html', employee=employee)

# 직원 삭제
@app.route('/delete/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    employees = load_employees()
    employees = [emp for emp in employees if emp['id'] != employee_id]
    save_employees(employees)
    
    flash('직원이 삭제되었습니다.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Debug mode should only be enabled in development
    # Set environment variable FLASK_DEBUG=1 for development
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
