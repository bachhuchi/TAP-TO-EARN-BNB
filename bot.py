import logging
import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# TOKEN CỦA BẠN
TOKEN = "8253603444:AAH--UQMJbx-ja8Z6Di92FnDy-agpTT0mQw"
WEB_APP_URL = "https://bank-mini-app.vercel.app"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ========== LỆNH /start ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Hiển thị menu chính với nút mở Mini App"""
    
    keyboard = [
        [InlineKeyboardButton(
            "🚀 MỞ APP KIẾM BNB", 
            web_app=WebAppInfo(url=WEB_APP_URL)
        )],
        [
            InlineKeyboardButton("💰 Cách kiếm BNB", callback_data="earn"),
            InlineKeyboardButton("📋 Nhiệm vụ", callback_data="tasks")
        ],
        [
            InlineKeyboardButton("🏧 Rút BNB", callback_data="withdraw_info"),
            InlineKeyboardButton("📊 Tỉ giá", callback_data="price")
        ],
        [
            InlineKeyboardButton("👥 Nhóm hỗ trợ", url="https://t.me/+xxx"),
            InlineKeyboardButton("📞 Liên hệ", callback_data="contact")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = """
🚀 *TAP TO EARN BNB - KIẾM TIỀN MỖI NGÀY*

*Cách hoạt động:*
1. *TAP:* Nhấn nút trong app → +0.00000012 BNB/tap
2. *NHIỆM VỤ:* Hoàn thành task → thưởng lớn
3. *RÚT:* Đổi BNB về ví cá nhân

*📊 Tỷ giá:* 1 BNB = 948 USDT
*💸 Tối thiểu rút:* 0.0008 BNB

Nhấn *MỞ APP KIẾM BNB* để bắt đầu!
"""
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# ========== XỬ LÝ WEB APP DATA ==========
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Nhận dữ liệu từ Mini App khi user rút tiền"""
    try:
        data = json.loads(update.effective_message.web_app_data.data)
        user_id = update.effective_user.id
        
        if data.get('action') == 'withdraw_bnb':
            # Xử lý yêu cầu rút BNB
            tx_id = f"TX{int(datetime.now().timestamp())}"
            
            # Lưu thông tin giao dịch
            withdrawal_data = {
                'user_id': user_id,
                'tx_id': tx_id,
                'wallet': data.get('wallet_address'),
                'amount': data.get('amount'),
                'usd_value': data.get('usd_value'),
                'status': 'pending',
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Gửi xác nhận cho user
            await update.message.reply_text(
                f"✅ *YÊU CẦU RÚT TIỀN ĐÃ ĐƯỢC TIẾP NHẬN!*\n\n"
                f"📋 *Mã giao dịch:* `{tx_id}`\n"
                f"💰 *Số lượng:* {data.get('amount')} BNB\n"
                f"💵 *Giá trị:* ${data.get('usd_value'):.2f}\n"
                f"📤 *Ví nhận:* `{data.get('wallet_address')[:10]}...{data.get('wallet_address')[-6:]}`\n\n"
                f"⏳ *Trạng thái:* Đang xử lý\n"
                f"🕐 *Thời gian:* 5-30 phút\n\n"
                f"Bạn sẽ nhận được thông báo khi giao dịch hoàn tất.",
                parse_mode='Markdown'
            )
            
            # Gửi thông báo cho admin (nếu có)
            await notify_admin(context, withdrawal_data, user_id)
            
    except Exception as e:
        logging.error(f"Lỗi xử lý web app data: {e}")

async def notify_admin(context: ContextTypes.DEFAULT_TYPE, data, user_id):
    """Gửi thông báo cho admin về yêu cầu rút tiền"""
    try:
        # Thay YOUR_ADMIN_ID bằng ID Telegram của bạn
        admin_id = "YOUR_ADMIN_ID"
        
        admin_message = f"""
⚠️ *CÓ YÊU CẦU RÚT BNB MỚI*

👤 User ID: `{user_id}`
📋 Mã giao dịch: `{data['tx_id']}`
💰 Số lượng: {data['amount']} BNB
💵 Giá trị: ${data['usd_value']:.2f}
📤 Ví nhận: `{data['wallet']}`
🕐 Thời gian: {data['timestamp']}
        """
        
        await context.bot.send_message(
            chat_id=admin_id,
            text=admin_message,
            parse_mode='Markdown'
        )
    except:
        pass

# ========== CÁC LỆNH KHÁC ==========
async def earn_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Thông tin cách kiếm BNB"""
    info_text = """
💰 *CÁCH KIẾM BNB*

*1. TAP HẰNG NGÀY:*
• Mỗi tap: +0.00000012 BNB
• Tối đa: 1000 tap/ngày
• Tổng: 0.00012 BNB/ngày

*2. XEM QUẢNG CÁO:*
• 30 phút được xem 10 lần
• Mỗi lần: +500 tap
• Tổng: 5,000 tap = 0.0006 BNB

*3. NHẤN LINK:*
• Link 1: https://vndshare.net/g3143511093
  → +1000 tap (1 lần/ngày)
• Link 2: https://vnshare.cc/g4177542121
  → +1000 tap (1 lần/ngày)

*4. THAM GIA NHÓM:*
• +10,000 tap (1 lần)

*5. YOUTUBE CODE:*
• +100,000 tap (1 lần)

*6. VƯỢT LINK XÁC MINH:*
• +10,000,000 tap (1 lần)

*TỔNG KIẾM TỐI ĐA/NGÀY:*
• Từ tap: 0.00012 BNB
• Từ quảng cáo: 0.0006 BNB
• Từ link: 0.00024 BNB
• → Tổng: ~0.00096 BNB/ngày

*Mở Mini App để bắt đầu kiếm ngay!*
"""
    
    keyboard = [[InlineKeyboardButton("🚀 Mở App để kiếm", web_app=WebAppInfo(url=WEB_APP_URL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        info_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def withdraw_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Thông tin rút tiền"""
    withdraw_text = """
🏧 *THÔNG TIN RÚT BNB*

*ĐIỀU KIỆN:*
• Tối thiểu: 0.0008 BNB
• Phí mạng: 0.00005 BNB
• Thời gian: 5-30 phút

*HƯỚNG DẪN RÚT:*
1. Mở Mini App
2. Tích lũy đủ 0.0008 BNB
3. Nhấn nút "RÚT BNB VỀ VÍ"
4. Nhập địa chỉ ví BEP20
5. Xác nhận giao dịch

*LƯU Ý:*
• Chỉ hỗ trợ ví BEP20 (Binance Smart Chain)
• Kiểm tra kỹ địa chỉ ví trước khi rút
• Tỷ giá: 1 BNB = 948 USDT (cập nhật 20 phút/lần)

*VÍ HỖ TRỢ:*
• Trust Wallet
• Metamask
• Binance Wallet
• Safepal
"""
    
    keyboard = [[InlineKeyboardButton("🚀 Mở App để rút", web_app=WebAppInfo(url=WEB_APP_URL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        withdraw_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý callback từ nút"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "earn":
        await earn_info(query, context)
    elif query.data == "withdraw_info":
        await withdraw_info(query, context)
    elif query.data == "price":
        await query.message.reply_text(
            "💎 *TỶ GIÁ BNB HIỆN TẠI*\n\n"
            "1 BNB = *948 USDT*\n"
            "1 BNB ≈ *23,000,000 VND*\n\n"
            "📈 Biến động 24h: +2.5%\n"
            "🔄 Cập nhật: 20 phút/lần\n\n"
            "Giá có thể thay đổi theo thị trường.",
            parse_mode='Markdown'
        )
    elif query.data == "tasks":
        await query.message.reply_text(
            "📋 *DANH SÁCH NHIỆM VỤ*\n\n"
            "1. *Tap hàng ngày* - 1000 tap\n"
            "2. *Xem quảng cáo* - 10 lần/ngày\n"
            "3. *Nhấn link VNDShare* - 1 lần/ngày\n"
            "4. *Nhấn link VNShare* - 1 lần/ngày\n"
            "5. *Tham gia nhóm* - 1 lần\n"
            "6. *Nhập code Youtube* - 1 lần\n"
            "7. *Xác minh tài khoản* - 1 lần\n\n"
            "Mở Mini App để làm nhiệm vụ!",
            parse_mode='Markdown'
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý tin nhắn thường"""
    text = update.message.text.lower()
    
    if any(word in text for word in ['chào', 'hello', 'hi']):
        await update.message.reply_text("👋 Chào bạn! Gõ /start để xem menu")
    
    elif any(word in text for word in ['kiếm bnb', 'earn', 'kiếm tiền']):
        await earn_info(update, context)
    
    elif any(word in text for word in ['rút bnb', 'withdraw', 'rut tien']):
        await withdraw_info(update, context)
    
    elif any(word in text for word in ['tỉ giá', 'giá bnb', 'price']):
        await update.message.reply_text(
            "💎 1 BNB = 948 USDT ≈ 23,000,000 VND\n"
            "Cập nhật 20 phút/lần",
            parse_mode='Markdown'
        )
    
    elif any(word in text for word in ['link', 'vndshare', 'vnshare']):
        await update.message.reply_text(
            "🔗 *CÁC LINK KIẾM TAP:*\n\n"
            "1. *VNDShare:* https://vndshare.net/g3143511093\n"
            "   → +1000 tap (1 lần/ngày)\n\n"
            "2. *VNShare:* https://vnshare.cc/g4177542121\n"
            "   → +1000 tap (1 lần/ngày)\n\n"
            "Nhấn link → Quay lại App → Nhận thưởng",
            parse_mode='Markdown'
        )
    
    else:
        keyboard = [[InlineKeyboardButton("🚀 Mở App", web_app=WebAppInfo(url=WEB_APP_URL))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🤖 *TAP TO EARN BNB BOT*\n\n"
            "Các lệnh:\n"
            "• /start - Menu chính\n"
            "• /earn - Cách kiếm BNB\n"
            "• /withdraw - Hướng dẫn rút\n"
            "• /price - Tỉ giá BNB\n\n"
            "Hoặc gõ: 'kiếm bnb', 'rút tiền', 'tỉ giá'",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

# ========== CHẠY BOT ==========
def main():
    """Hàm chính chạy bot"""
    application = Application.builder().token(TOKEN).build()
    
    # Thêm handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("earn", earn_info))
    application.add_handler(CommandHandler("withdraw", withdraw_info))
    application.add_handler(CommandHandler("price", withdraw_info))
    
    # Web App data handler
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    
    # Callback handler
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    # Message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("=" * 50)
    print("🚀 TAP TO EARN BNB BOT ĐANG CHẠY...")
    print(f"🌐 Mini App: {WEB_APP_URL}")
    print(f"🤖 Bot: @bankofvnbot")
    print("=" * 50)
    
    # Chạy bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()