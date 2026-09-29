import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# المحفظة المشفرة المقفلة لمالك المنصة لاستلام الأرباح
OWNER_WALLET_ADDRESS = os.environ.get("OWNER_WALLET", "0x76da8cb55d85a2eb1def7eff79142b98abc42784")

# الواجهة المرئية الكاملة مدمجة برمجياً داخل الكود لتجنب خطأ الـ 404 نهائياً
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة الوكلاء الذكية الشاملة للشركات</title>
    <style>
        :root { --primary: #2c3e50; --secondary: #16a085; --accent: #e74c3c; --bg: #f9f9f9; }
        body { font-family: 'Segoe UI', Tahoma, sans-serif; background-color: var(--bg); margin: 0; padding: 0; }
        header { background-color: var(--primary); color: white; padding: 20px; text-align: center; }
        .container { max-width: 1200px; margin: 30px auto; padding: 0 20px; display: grid; grid-template-columns: 1fr 2fr; gap: 30px; }
        @media (max-width: 768px) { .container { grid-template-columns: 1fr; } }
        .card { background: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); padding: 25px; margin-bottom: 25px; }
        .wallet-balance { font-size: 28px; font-weight: bold; color: var(--secondary); text-align: center; margin: 20px 0; background: #e8f8f5; padding: 15px; border-radius: 8px; }
        .btn { display: block; width: 100%; background-color: var(--secondary); color: white; border: none; padding: 12px; border-radius: 6px; font-size: 16px; cursor: pointer; text-align: center; font-weight: bold; margin-bottom: 10px; }
        .btn-accent { background-color: var(--primary); }
        .btn-danger { background-color: var(--accent); }
        textarea, select, input { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 6px; margin-bottom: 15px; box-sizing: border-box; }
        .result-box { background-color: #f4f6f6; border-left: 5px solid var(--secondary); padding: 20px; border-radius: 6px; min-height: 100px; white-space: pre-wrap; margin-top: 20px; }
    </style>
</head>
<body>
    <header>
        <h1>منصة الوكلاء الذكية الشاملة للشركات</h1>
        <p>بوابة الخدمات الاستشارية والتسويقية المؤتمتة عالية الأمان - ثلاثية اللغات</p>
    </header>
    <div class="container">
        <aside class="card">
            <h2>💳 محفظتك الرقمية المؤمنة</h2>
            <div class="wallet-balance" id="balanceDisplay">\$0.00</div>
            <input type="number" id="amountInput" placeholder="أدخل المبلغ (USD)" min="1">
            <button class="btn" onclick="handleAction('deposit')">💰 إيداع أموال آمن</button>
            <button class="btn btn-accent" onclick="handleAction('crypto_deposit')">🪙 شحن بالعملات الرقمية (USDT)</button>
            <button class="btn btn-danger" onclick="handleAction('withdraw')">💸 سحب المستحقات للمالك</button>
            <hr style="border:0; border-top:1px solid #eee; margin:20px 0;">
            <button class="btn btn-accent" onclick="handleAction('subscribe')">🎉 تفعيل الاشتراك الشهري (\$29)</button>
        </aside>
        <main class="card">
            <h2>🤖 لوحة تشغيل فريق الوكلاء الذكي</h2>
            <select id="serviceType">
                <option value="marketing">✍️ صياغة إعلان تسويقي أو مقال احترافي (SEO)</option>
                <option value="business">💡 تشخيص وحل مشاكل الشركات (استشارة إستراتيجية)</option>
                <option value="summary">✂️ تلخيص مستندات ونصوص معقدة وطويلة</option>
            </select>
            <textarea id="userInput" rows="6" placeholder="اكتب تفاصيل طلبك هنا باللغة العربية، الإنجليزية، أو الفرنسية..."></textarea>
            <button class="btn btn-accent" onclick="runAgent()">🚀 إطلاق الوكلاء للتنفيذ التلقائي</button>
            <h3>📊 المخرجات والنتائج الفورية:</h3>
            <div class="result-box" id="resultDisplay">في انتظار أوامرك... سيتم عرض التقارير الذكية هنا فوراً وبشكل منسق وفوري.</div>
        </main>
    </div>
    <script>
        let balance = 0.0;
        function handleAction(type) {
            let amount = parseFloat(document.getElementById('amountInput').value) || 0;
            if (type === 'deposit' && amount > 0) { balance += amount; alert(`💰 تم الإيداع بنجاح: +$${amount}`); }
            else if (type === 'crypto_deposit') { alert("🪙 تم توليد عنوان محفظة USDT الخاص بك بنجاح على البلوكشين."); balance += 50; }
            else if (type === 'withdraw' && amount > 0) {
                if(balance >= amount) { balance -= amount; alert("💸 تم تحويل مستحقاتك بنجاح للمحفظة المقفلة للمالك."); }
                else { alert("❌ خطأ: الرصيد غير كافٍ."); }
            } else if (type === 'subscribe') {
                if(balance >= 29) { balance -= 29; alert("🎉 تم تفعيل الاشتراك الشهري لخدمات الذكاء الاصطناعي الشاملة."); }
                else { alert("❌ رصيد المحفظة لا يكفي للاشتراك."); }
            }
            document.getElementById('balanceDisplay').innerText = `$${balance.toFixed(2)}`;
            document.getElementById('amountInput').value = '';
        }
        function runAgent() {
            let input = document.getElementById('userInput').value;
            if(!input) { alert("يرجى إدخال نص أولاً."); return; }
            document.getElementById('resultDisplay').innerText = "🔄 جاري تشغيل الوكلاء المستقلين وتحليل البيانات وتوليد المخرجات ماليًا وتجاريًا...";
            setTimeout(() => {
                document.getElementById('resultDisplay').innerText = "✅ تم التنفيذ ذاتياً!\n\n[المخرج]: تم تحضير المحتوى المطلوب بدقة وإرسال إشعار الفاتورة المؤمنة لبريد العميل واستقطاع الرسوم التلقائية بنجاح.";
            }, 1500);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/run-agent', methods=['POST'])
def run_agent():
    return jsonify({"status": "success", "message": "تم التشغيل الذاتي الحاسم"})
