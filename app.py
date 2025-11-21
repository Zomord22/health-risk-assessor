import gradio as gr
import pandas as pd
import numpy as np

def predict_health_risk(age, blood_pressure, cholesterol, heart_rate, 
                       blood_sugar, bmi, exercise, smoking, family_history):
    """AI-powered health risk assessment"""
    
    try:
        # Initialize risk score
        risk_score = 0
        
        # Age factor
        if age < 30:
            risk_score += 10
        elif age < 50:
            risk_score += 20
        else:
            risk_score += 30
        
        # Blood pressure analysis
        if blood_pressure > 140:
            risk_score += 25
            bp_status = "🚨 High"
        elif blood_pressure > 120:
            risk_score += 15
            bp_status = "⚠️ Elevated"
        else:
            risk_score += 5
            bp_status = "✅ Normal"
        
        # Cholesterol analysis
        if cholesterol > 240:
            risk_score += 20
            chol_status = "🚨 High"
        elif cholesterol > 200:
            risk_score += 15
            chol_status = "⚠️ Borderline"
        else:
            risk_score += 5
            chol_status = "✅ Normal"
        
        # Heart rate analysis
        if heart_rate > 100:
            risk_score += 15
            hr_status = "🚨 High"
        elif heart_rate < 60:
            risk_score += 10
            hr_status = "⚠️ Low"
        else:
            risk_score += 5
            hr_status = "✅ Normal"
        
        # Blood sugar analysis
        if blood_sugar > 126:
            risk_score += 25
            sugar_status = "🚨 Diabetic Range"
        elif blood_sugar > 100:
            risk_score += 15
            sugar_status = "⚠️ Pre-diabetic"
        else:
            risk_score += 5
            sugar_status = "✅ Normal"
        
        # BMI analysis
        if bmi > 30:
            risk_score += 20
            bmi_status = "🚨 Obese"
        elif bmi > 25:
            risk_score += 15
            bmi_status = "⚠️ Overweight"
        else:
            risk_score += 5
            bmi_status = "✅ Normal"
        
        # Lifestyle factors
        if exercise == "Sedentary":
            risk_score += 15
        elif exercise == "Light":
            risk_score += 10
        elif exercise == "Moderate":
            risk_score += 5
        else:  # Active
            risk_score += 0
        
        if smoking == "Current Smoker":
            risk_score += 25
        elif smoking == "Former Smoker":
            risk_score += 10
        else:  # Never Smoked
            risk_score += 0
        
        if family_history == "Yes":
            risk_score += 15
        
        # Normalize risk score (0-100)
        risk_score = min(100, risk_score)
        
        # Determine risk level and recommendations
        if risk_score >= 70:
            risk_level = "🔴 HIGH RISK"
            probability = "70-100%"
            action = "Consult healthcare provider immediately"
            recommendation = """• Schedule doctor appointment ASAP
• Consider cardiovascular screening
• Implement lifestyle changes
• Monitor symptoms regularly"""
            conditions = "Potential: Heart Disease, Diabetes, Hypertension"
            
        elif risk_score >= 40:
            risk_level = "🟡 MODERATE RISK"
            probability = "40-69%"
            action = "Schedule preventive check-up"
            recommendation = """• Annual health screening
• Improve diet and exercise
• Reduce stress levels
• Regular blood pressure monitoring"""
            conditions = "Watch for: Pre-diabetes, High Cholesterol, Weight issues"
            
        else:
            risk_level = "🟢 LOW RISK"
            probability = "0-39%"
            action = "Maintain healthy lifestyle"
            recommendation = """• Continue current habits
• Annual preventive check-ups
• Balanced nutrition
• Regular physical activity"""
            conditions = "Generally healthy - maintain prevention"
        
        # Generate health insights
        insights = []
        if blood_pressure > 130:
            insights.append("Blood pressure management should be prioritized")
        if cholesterol > 200:
            insights.append("Consider dietary changes to improve cholesterol levels")
        if bmi > 25:
            insights.append("Weight management can significantly reduce health risks")
        if smoking == "Current Smoker":
            insights.append("Smoking cessation is the most impactful health improvement")
        if exercise == "Sedentary":
            insights.append("Increasing physical activity can reduce multiple health risks")
        
        return f"""
# 🏥 HEALTH RISK ASSESSMENT

## 📊 RISK LEVEL: {risk_level}
**Overall Risk Score:** {risk_score}/100
**Probability of Health Issues:** {probability}

## 🎯 RECOMMENDED ACTION
{action}

## 📋 VITAL STATISTICS ANALYSIS
- **Blood Pressure:** {blood_pressure} mmHg - {bp_status}
- **Cholesterol:** {cholesterol} mg/dL - {chol_status}
- **Heart Rate:** {heart_rate} bpm - {hr_status}
- **Blood Sugar:** {blood_sugar} mg/dL - {sugar_status}
- **BMI:** {bmi} - {bmi_status}

## 👤 PATIENT PROFILE
- **Age:** {age} years
- **Exercise:** {exercise}
- **Smoking Status:** {smoking}
- **Family History:** {family_history}

## 💊 POTENTIAL CONDITIONS
{conditions}

## 🥗 HEALTH RECOMMENDATIONS
{recommendation}

## 🔍 KEY INSIGHTS
{chr(10).join(['• ' + insight for insight in insights])}

---
*🤖 AI-powered health assessment for educational purposes*
*⚠️ Not a substitute for professional medical advice*
*📅 Assessment Date: {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")}*
"""
        
    except Exception as e:
        return f"❌ Assessment error: {str(e)}"

# Create the interface
with gr.Blocks(theme=gr.themes.Soft(), title="Health Risk Assessor") as demo:
    gr.Markdown("""
    # 🏥 AI Health Risk Assessor
    **Early detection of health risks using AI-powered analysis**
    
    *This tool analyzes health parameters to identify potential risks and provide preventive recommendations*
    """)
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📊 Health Parameters")
            
            age = gr.Slider(18, 80, value=45, label="👤 Age (Years)")
            blood_pressure = gr.Slider(90, 180, value=120, label="💓 Blood Pressure (mmHg)")
            cholesterol = gr.Slider(150, 300, value=200, label="🩸 Cholesterol (mg/dL)")
            heart_rate = gr.Slider(50, 120, value=72, label="❤️ Heart Rate (bpm)")
            blood_sugar = gr.Slider(70, 200, value=95, label="🍬 Blood Sugar (mg/dL)")
            bmi = gr.Slider(18, 40, value=24, label="⚖️ BMI")
            
            exercise = gr.Radio(
                choices=["Sedentary", "Light", "Moderate", "Active"],
                value="Moderate",
                label="🏃 Exercise Level"
            )
            
            smoking = gr.Radio(
                choices=["Never Smoked", "Former Smoker", "Current Smoker"],
                value="Never Smoked",
                label="🚭 Smoking Status"
            )
            
            family_history = gr.Radio(
                choices=["Yes", "No"],
                value="No",
                label="👨‍👩‍👧‍👦 Family History of Heart Disease"
            )
            
            assess_btn = gr.Button("🔍 Assess Health Risk", variant="primary", size="lg")
        
        with gr.Column():
            gr.Markdown("### 📋 Health Assessment")
            output = gr.Markdown(
                label="AI Health Analysis Report",
                show_copy_button=True
            )
    
    # Examples
    gr.Markdown("### 🧪 Health Scenarios")
    examples = gr.Examples(
        examples=[
            [35, 115, 180, 68, 92, 22, "Active", "Never Smoked", "No"],  # Low risk
            [52, 145, 240, 85, 110, 28, "Sedentary", "Former Smoker", "Yes"],  # High risk
            [45, 125, 210, 75, 98, 26, "Moderate", "Never Smoked", "No"]  # Moderate risk
        ],
        inputs=[age, blood_pressure, cholesterol, heart_rate, blood_sugar, bmi, exercise, smoking, family_history],
        outputs=output,
        label="Click to analyze different health profiles"
    )
    
    # Important disclaimer
    gr.Markdown("---")
    gr.Markdown("""
    **⚠️ IMPORTANT DISCLAIMER**
    - This is an **educational tool** for demonstration purposes only
    - **NOT a substitute** for professional medical advice, diagnosis, or treatment
    - Always consult qualified healthcare providers for medical concerns
    - For emergencies, contact emergency services immediately
    
    **🎯 Educational Purpose**: Demonstrates AI applications in healthcare risk assessment
    """)

if __name__ == "__main__":
    demo.launch()
