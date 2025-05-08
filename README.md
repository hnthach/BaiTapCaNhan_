Báo cáo đồ án cá nhân (8-puzzles)

1. Mục tiêu
	```
	Mục tiêu của bài tập cá nhân này là áp dụng các nhóm thuật toán trong lĩnh vực Trí tuệ nhân tạo để giải quyết bài toán 8-Puzzle
	, một bài toán cổ điển trong AI thuộc loại tìm kiếm trạng thái. Thông qua việc triển khai và so sánh hiệu quả giữa các nhóm thuật
	toán như tìm kiếm không thông tin (uninformed search), tìm kiếm có thông tin (informed search), tìm kiếm cục bộ (local search),
	giải quyết ràng buộc (CSP) và học tăng cường (reinforcement learning), bài tập nhằm đạt được các mục tiêu cụ thể sau:  
		- Hiểu rõ cách biểu diễn bài toán 8-Puzzle dưới dạng bài toán tìm kiếm trong không gian trạng thái.
		- Nắm bắt được nguyên lý hoạt động, ưu điểm và hạn chế của từng nhóm thuật toán AI thông qua việc áp dụng vào cùng một bài toán cụ thể.
		- Triển khai thực tế các thuật toán giải bài toán 8-Puzzle và xây dựng giao diện mô phỏng quá trình giải.
		- So sánh, đánh giá hiệu suất giữa các thuật toán về số bước giải, thời gian thực thi, và khả năng tìm lời giải tối ưu.
		- Tăng cường khả năng phân tích và lựa chọn thuật toán phù hợp cho các bài toán tương tự trong thực tế.
	```
2. Nội dung  

	2.1. Các thuật toán tìm kiếm không có thông tin ( Uninformed Search )
   ```
   2.1.1 Các thành phần chính của bài toán tìm kiếm và solution
   a. BFS
   * Hình ảnh gif mô tả thuật toán: ![BFS](https://github.com/user-attachments/assets/31a8c27b-4e7e-4b03-8477-9080f74e4fc7)
   - Các thành phần chính:
	   + Hàng đợi (Queue):
		   . Chức năng: Lưu trữ các trạng thái cần xét, kèm theo đường đi từ trạng thái bắt đầu, theo nguyên tắc FIFO (First-In-First-Out)
		   . Trong code: Sử dụng deque từ thư viện collections để tối ưu hiệu suất khi thêm/xóa đầu cuối
	   + Tập hợp đã thăm (Visited Set):
		   . Chức năng: Lưu các trạng thái đã được duyệt nhằm tránh lặp lại, tiết kiệm thời gian và bộ nhớ
		   . Trong code: Dùng set để kiểm tra và thêm trạng thái với độ phức tạp trung bình O(1)
	   + Hàm tìm trạng thái lân cận:
		   . Chức năng: Từ vị trí ô trống hiện tại, tạo ra các trạng thái hợp lệ bằng cách di chuyển theo 4 hướng (trên, dưới, trái, phải)
		   . Trong code: Tính toán vị trí mới và gọi hàm swap_tiles để tạo trạng thái mới
	   + Vòng lặp chính:
		   . Lấy trạng thái đầu tiên từ hàng đợi
		   . Kiểm tra nếu trạng thái đó là trạng thái mục tiêu
		   . Nếu chưa, sinh trạng thái kế tiếp và thêm vào hàng đợi nếu chưa từng xét
   - Solution từ BFS:
	   + Đặc điểm của lời giải:
		   . Tính đầy đủ: BFS luôn đảm bảo tìm ra lời giải nếu tồn tại vì duyệt theo bề rộng
		   . Tính tối ưu: Luôn tìm được đường đi ngắn nhất tính theo số bước chuyển trạng thái
	   + Biểu diễn lời giải trong chương trình:
		   . Dạng đường đi: Lưu lại chuỗi các trạng thái từ điểm bắt đầu đến mục tiêu trong biến path
		   . Cập nhật đường đi: Mỗi lần tạo trạng thái mới, nối vào đường đi hiện tại để bảo toàn thứ tự
	   + Hiển thị lời giải trên giao diện:
		   . Cách hiển thị: Từng trạng thái trong đường đi được hiển thị lần lượt, có độ trễ giữa các bước để quan sát rõ ràng
		   . Thông số điều khiển: Độ trễ được điều chỉnh qua biến STEP_DELAY
	   + Đánh giá hiệu suất thuật toán:
		   . Thời gian thực thi: Được tính từ lúc bắt đầu đến khi tìm ra lời giải với đồ phức tạp O(b^d) và hiển thị trên giao diện
   b. DFS
   * Hình ảnh gif mô tả thuật toán: ![DFS](https://github.com/user-attachments/assets/75eaded7-e057-41d3-b0e8-8237aa74e1d2)
   

   ```

