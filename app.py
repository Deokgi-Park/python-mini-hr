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
SALARY_FILE = 'salaries.json'

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

# 급여 데이터 로드
def load_salaries():
    if os.path.exists(SALARY_FILE):
        with open(SALARY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# 급여 데이터 저장
def save_salaries(salaries):
    with open(SALARY_FILE, 'w', encoding='utf-8') as f:
        json.dump(salaries, f, ensure_ascii=False, indent=2)

# 남은 연차 계산
def calculate_remaining_leave(annual_leave, used_leave):
    return (annual_leave or 0) - (used_leave or 0)

# 메인 페이지 - 직원 목록
@app.route('/')
def index():
    employees = load_employees()
    # 남은 연차 계산하여 추가
    for emp in employees:
        emp['remaining_leave'] = calculate_remaining_leave(
            emp.get('annual_leave', 0), 
            emp.get('used_leave', 0)
        )
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
            'ssn': request.form.get('ssn'),
            'department': request.form.get('department'),
            'position': request.form.get('position'),
            'hire_date': request.form.get('hire_date'),
            'resignation_date': request.form.get('resignation_date') or None,
            'address': request.form.get('address'),
            'personal_email': request.form.get('personal_email'),
            'work_email': request.form.get('work_email'),
            'personal_phone': request.form.get('personal_phone'),
            'work_phone': request.form.get('work_phone'),
            'has_insurance': request.form.get('has_insurance') == 'on',
            'salary_bank': request.form.get('salary_bank'),
            'salary_account': request.form.get('salary_account'),
            'years_of_service': int(request.form.get('years_of_service') or 0),
            'annual_leave': int(request.form.get('annual_leave') or 0),
            'used_leave': int(request.form.get('used_leave') or 0),
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
    
    # 남은 연차 계산
    employee['remaining_leave'] = calculate_remaining_leave(
        employee.get('annual_leave', 0), 
        employee.get('used_leave', 0)
    )
    
    # 해당 직원의 급여 정보 로드
    salaries = load_salaries()
    employee_salaries = [s for s in salaries if s['employee_id'] == employee_id]
    
    # 연도 목록 생성 (급여 데이터가 있는 연도들)
    years = sorted(list(set([s['year'] for s in employee_salaries])), reverse=True)
    
    # 선택된 연도 (기본값: 가장 최근 연도 또는 현재 연도)
    selected_year = request.args.get('year', type=int)
    if not selected_year:
        selected_year = years[0] if years else datetime.now().year
    
    # 선택된 연도의 급여 정보
    salary_info = next((s for s in employee_salaries if s['year'] == selected_year), None)
    
    return render_template('employee_detail.html', 
                         employee=employee, 
                         salary_info=salary_info,
                         years=years,
                         selected_year=selected_year)

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
        employee['ssn'] = request.form.get('ssn')
        employee['department'] = request.form.get('department')
        employee['position'] = request.form.get('position')
        employee['hire_date'] = request.form.get('hire_date')
        employee['resignation_date'] = request.form.get('resignation_date') or None
        employee['address'] = request.form.get('address')
        employee['personal_email'] = request.form.get('personal_email')
        employee['work_email'] = request.form.get('work_email')
        employee['personal_phone'] = request.form.get('personal_phone')
        employee['work_phone'] = request.form.get('work_phone')
        employee['has_insurance'] = request.form.get('has_insurance') == 'on'
        employee['salary_bank'] = request.form.get('salary_bank')
        employee['salary_account'] = request.form.get('salary_account')
        employee['years_of_service'] = int(request.form.get('years_of_service') or 0)
        employee['annual_leave'] = int(request.form.get('annual_leave') or 0)
        employee['used_leave'] = int(request.form.get('used_leave') or 0)
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

# 급여 정보 추가/수정
@app.route('/salary/<int:employee_id>', methods=['GET', 'POST'])
def manage_salary(employee_id):
    employees = load_employees()
    employee = next((emp for emp in employees if emp['id'] == employee_id), None)
    
    if employee is None:
        flash('직원을 찾을 수 없습니다.', 'error')
        return redirect(url_for('index'))
    
    salaries = load_salaries()
    
    if request.method == 'POST':
        year = int(request.form.get('year'))
        
        # 해당 직원의 해당 연도 급여 정보 찾기
        salary_entry = next((s for s in salaries if s['employee_id'] == employee_id and s['year'] == year), None)
        
        salary_data = {
            'employee_id': employee_id,
            'year': year,
            'month_01': int(request.form.get('month_01') or 0),
            'month_02': int(request.form.get('month_02') or 0),
            'month_03': int(request.form.get('month_03') or 0),
            'month_04': int(request.form.get('month_04') or 0),
            'month_05': int(request.form.get('month_05') or 0),
            'month_06': int(request.form.get('month_06') or 0),
            'month_07': int(request.form.get('month_07') or 0),
            'month_08': int(request.form.get('month_08') or 0),
            'month_09': int(request.form.get('month_09') or 0),
            'month_10': int(request.form.get('month_10') or 0),
            'month_11': int(request.form.get('month_11') or 0),
            'month_12': int(request.form.get('month_12') or 0),
        }
        
        if salary_entry:
            # 업데이트
            salary_entry.update(salary_data)
        else:
            # 새로 추가
            salaries.append(salary_data)
        
        save_salaries(salaries)
        flash('급여 정보가 저장되었습니다.', 'success')
        return redirect(url_for('employee_detail', employee_id=employee_id, year=year))
    
    # GET 요청 - 급여 입력 폼 표시
    year = request.args.get('year', type=int, default=datetime.now().year)
    salary_info = next((s for s in salaries if s['employee_id'] == employee_id and s['year'] == year), None)
    
    return render_template('manage_salary.html', employee=employee, salary_info=salary_info, year=year)

if __name__ == '__main__':
    # Debug mode should only be enabled in development
    # Set environment variable FLASK_DEBUG=1 for development
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
