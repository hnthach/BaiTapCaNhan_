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
   
   c. IDDFS
      * Hình ảnh gif mô tả thuật toán: (https://github.com/hnthach/BaiTapCaNhan_/blob/main/%E1%BA%A2nh_GIF/1.%20Uninformed%20Search/IDDFS.gif?raw=true)
   - Các thành phần chính:
	   + Hàm chính: iddfs(start, goal)
		   . Là một vòng lặp vô hạn (while True) thực hiện tìm kiếm sâu dần theo từng mức độ sâu.
		   . Mỗi vòng lặp sẽ gọi dfs(start, goal, depth) với giới hạn độ sâu hiện tại.
		   . Nếu dfs trả về lời giải (path), thì kết thúc ngay.
		   . Nếu không, độ sâu được tăng thêm 1 và thử lại cho đến khi vượt quá mức giới hạn tối đa (depth > 31) → trả về None.
	   + Chiến lược tìm kiếm
		   . Bắt đầu tìm kiếm với độ sâu = 0 (chỉ kiểm tra trạng thái ban đầu).
		   . Dần dần tăng độ sâu lên 1, 2, 3,... cho đến khi tìm được lời giải hoặc vượt giới hạn độ sâu cho phép.
		   . Mỗi lần đều sử dụng DFS có giới hạn độ sâu (depth-limited DFS) để tránh đi quá sâu hoặc bị lặp vô hạn.
	   + Hàm phụ: dfs(start, goal, max_depth)
		   . Duyệt theo chiều sâu (Depth-First) nhưng chỉ trong phạm vi độ sâu giới hạn.
		   . Không dùng visited để tránh cản trở việc lặp lại khi cần trong IDDFS.
		   . Trả về đường đi nếu tìm thấy mục tiêu trong phạm vi độ sâu, ngược lại trả về None.
   - Solution từ IDDFS:
	   + Tính đầy đủ (Completeness)
		   . IDDFS đảm bảo sẽ tìm ra lời giải nếu tồn tại (trong giới hạn độ sâu), vì duyệt toàn bộ không gian trạng thái tăng dần theo từng độ sâu.
	   + Tính tối ưu (Optimality)
		   . Luôn tìm được đường đi ngắn nhất (theo số bước) vì lời giải đầu tiên được phát hiện ở độ sâu nhỏ nhất.
	   + Hiệu quả về bộ nhớ (Memory Efficiency)
		   . Mỗi lần gọi DFS chỉ cần dùng bộ nhớ cho stack theo độ sâu hiện tại, không cần lưu visited toàn cục như BFS → rất tiết kiệm bộ nhớ.
	   + Chi phí tính toán lặp lại (Redundant Computation)
		   . Một số trạng thái có thể được duyệt lại nhiều lần ở các mức độ sâu khác nhau (trade-off giữa bộ nhớ và thời gian).
		   . Tuy nhiên, với các bài toán như 8-puzzle, việc này vẫn hợp lý do số lượng trạng thái hữu hạn và không quá lớn.
   
   d. UCS
   - Các thành phần chính:
	   + Hàng đợi ưu tiên (priority_queue)
		   . Chức năng: Lưu trữ các trạng thái cần xét, ưu tiên theo tổng chi phí từ trạng thái bắt đầu.
		   . Trong code: Sử dụng heapq để đảm bảo phần tử có chi phí nhỏ nhất được lấy ra trước. Mỗi phần tử có dạng (cost, state, path).
	   + Tập hợp đã thăm (visited)
		   . Chức năng: Tránh xét lại các trạng thái đã xử lý để tiết kiệm thời gian và bộ nhớ.
		   . Trong code: Dùng set để tra cứu nhanh, độ phức tạp trung bình O(1).
	   + Chiến lược mở rộng trạng thái
		   . Với mỗi trạng thái đang xét, tìm vị trí ô trống rồi tạo các trạng thái mới bằng cách di chuyển theo 4 hướng.
		   . Mỗi trạng thái mới sẽ được thêm vào hàng đợi với chi phí tăng thêm (ở đây: cost + 1, vì mỗi bước có cùng chi phí 1).
   - Solution từ UCS:
	   + Tính đầy đủ (Completeness)
		   . UCS luôn tìm được lời giải nếu có, vì nó mở rộng trạng thái theo chi phí tăng dần (tương tự BFS nhưng có trọng số).
	   + Tính tối ưu (Optimality)
		   . Đảm bảo tìm ra lời giải có chi phí thấp nhất (tối ưu nhất) – đặc biệt hiệu quả nếu các bước có trọng số khác nhau.
		   . Trong 8-puzzle này, các bước có chi phí bằng nhau (1) nên UCS hoạt động tương đương BFS nhưng vẫn đúng nguyên lý.
	   + Cách biểu diễn lời giải trong chương trình
		   . Mỗi lần mở rộng, đường đi được lưu lại qua biến path, được cập nhật bằng cách nối thêm trạng thái mới (path + [new_state]).
	   + Hiển thị lời giải trên giao diện (nếu có)
		   . Đường đi từ trạng thái bắt đầu đến đích có thể được hiển thị từng bước, có thể điều chỉnh độ trễ qua biến như STEP_DELAY (không có trong code hiện tại, 		     nhưng có thể thêm).
	   + Hiệu suất thuật toán
		   . Thời gian thực thi phụ thuộc vào độ sâu lời giải và số nhánh trung bình (b), với độ phức tạp O(b^d) (như BFS).
		   . Tuy nhiên, UCS mở rộng theo chi phí nên có thể hiệu quả hơn BFS nếu áp dụng vào bài toán có chi phí khác nhau giữa các bước.

   2.1.2 Hình ảnh gif so sánh các thuật toán trong nhóm thuật toán tìm kiếm không có thông tin
   https://github.com/hnthach/BaiTapCaNhan_/blob/main/%E1%BA%A2nh_GIF/1.%20Uninformed%20Search/SoSanhHieuXuat_Uninformed%20Search.gif?raw=true

   2.1.3 Nhận xét về hiệu suất các thuật toán
	   - BFS đảm bảo tìm ra lời giải ngắn nhất về số bước, nhưng tiêu tốn rất nhiều bộ nhớ do phải lưu toàn bộ trạng thái ở từng mức sâu. Với bài toán như 8-puzzle, BFS dễ bị giới hạn tài nguyên khi độ sâu tăng.
	   - DFS sử dụng ít bộ nhớ hơn do đi sâu theo nhánh, nhưng dễ bị lặp vô hạn và không đảm bảo tìm được lời giải ngắn nhất. Giới hạn độ sâu có thể giúp tránh lặp nhưng có nguy cơ bỏ sót lời giải.
	   - IDDFS khắc phục cả nhược điểm của BFS và DFS: tiết kiệm bộ nhớ, đồng thời vẫn tìm được lời giải ngắn nhất nhờ việc lặp DFS với độ sâu tăng dần.
	   - UCS tối ưu về chi phí thay vì độ dài đường đi. Khi chi phí mỗi bước giống nhau, UCS tương đương BFS. Tuy nhiên, UCS tiêu tốn bộ nhớ lớn do dùng hàng đợi ưu tiên để xử lý trạng thái theo tổng chi phí thấp nhất.
   
   ```
2.2 Các thuật toán tìm kiếm có thông tin (Informed Search)
```
2.2.1 Các thành phần chính của bài toán tìm kiếm và solution
a. Thuật toán A*

```
