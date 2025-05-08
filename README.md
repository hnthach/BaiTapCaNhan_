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
   * Hình ảnh gif mô tả thuật toán: (https://github.com/hnthach/BaiTapCaNhan_/blob/main/%E1%BA%A2nh_GIF/1.%20Uninformed%20Search/BFS.gif?raw=true)
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
   * Hình ảnh gif mô tả thuật toán: (https://github.com/hnthach/BaiTapCaNhan_/blob/main/%E1%BA%A2nh_GIF/1.%20Uninformed%20Search/DFS.gif?raw=true)
   - Các thành phần chính:
	   + Ngăn xếp (Stack):
		   . Chức năng: Lưu trữ các trạng thái cần xét kèm theo đường đi từ trạng thái bắt đầu, theo nguyên tắc LIFO (Last-In-First-Out).
		   . Trong code: Sử dụng list với cấu trúc (state, path, depth) và thao tác .pop() để lấy trạng thái cuối cùng đã thêm
	   + Tập hợp đã thăm (Visited Set):
		   . Trong DFS này: KKhông dùng visited set toàn cục mà chỉ kiểm tra trạng thái có trong path hiện tại để tránh lặp, giúp phù hợp với DFS giới hạn độ sâu và 		     IDDFS, đồng thời tiết kiệm bộ nhớ.
	   + Giới hạn độ sâu (Depth Limit):
		   . Chức năng: Ngăn DFS đi quá sâu vào một nhánh, đặc biệt hữu ích khi sử dụng trong IDDFS
		   . Trong code: Kiểm tra if depth >= max_depth để bỏ qua các nhánh vượt giới hạn
	   + Hàm tìm trạng thái lân cận:
		   . Giống BFS: Tìm vị trí ô trống và duyệt 4 hướng di chuyển (trên, dưới, trái, phải)
		   . Trong code: Dùng find_blank() để xác định vị trí, tính toán vị trí mới và gọi swap_tiles() để tạo new_state
   - Solution từ DFS:
	   + Đặc điểm của lời giải:
		   . Không đảm bảo tối ưu: Solution có thể dài hơn nhiều so với solution ngắn nhất mà BFS tìm được
		   . Phụ thuộc vào thứ tự duyệt: Thay đổi thứ tự duyệt các hướng (UP, DOWN, LEFT, RIGHT) sẽ cho solution khác nhau
                   . Có thể không tìm thấy lời giải: Nếu đặt max_depth quá nhỏ so với độ sâu lời giải, thuật toán sẽ bỏ qua lời giải đó
	   + Biểu diễn lời giải trong chương trình:
		   . Dạng đường đi: Tương tự BFS, sử dụng biến path để lưu chuỗi các trạng thái từ điểm bắt đầu đến đích
		   . Cập nhật đường đi: Mỗi khi tạo trạng thái mới, path + [new_state] được đưa vào stack để đảm bảo đúng thứ tự duyệt
	   + Hiển thị lời giải trên giao diện:
		   . Cách hiển thị: Mỗi trạng thái trong đường đi được vẽ lên giao diện với hiệu ứng chuyển tiếp rõ ràng
		   . Thông số điều khiển: Tốc độ chuyển trạng thái được điều chỉnh thông qua biến STEP_DELAY
	   + Đánh giá hiệu suất thuật toán:
		   . Thời gian thực thi: Phụ thuộc vào độ sâu tối đa max_depth và cấu trúc cây trạng thái; độ phức tạp trong trường hợp xấu là O(b^d), với b là branching 		    factor và d là độ sâu lời giải
   ```

