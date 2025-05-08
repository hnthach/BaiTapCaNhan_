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
* Hình ảnh gif mô tả thuật toán: (https://github.com/hnthach/BaiTapCaNhan_/blob/main/%E1%BA%A2nh_GIF/2.%20Informed%20Search/A_Star.gif?raw=true)
- Các thành phần chính:
	+ Hàm heuristic (Manhattan Distance)
		· Tính tổng khoảng cách hàng và cột giữa vị trí hiện tại và vị trí đích của mỗi ô
		· Là heuristic admissible nên đảm bảo không đánh giá thấp chi phí thực tế
	+ Hàng đợi ưu tiên (Priority Queue)
		· Luôn mở rộng trạng thái có tổng chi phí f(n) = g(n) + h(n) thấp nhất
		· Sử dụng heapq để đảm bảo truy xuất nhanh phần tử có f nhỏ nhất
	+ Tập trạng thái đã xét (Visited Set)
		· Tránh lặp lại trạng thái đã duyệt, giúp giảm thời gian và tiết kiệm bộ nhớ
		· Kiểm tra nhanh bằng set
	+ Hàm tạo trạng thái mới (Neighbor Generation)
		· Tạo trạng thái mới bằng cách di chuyển ô trống theo 4 hướng
		· Cập nhật chi phí g(n) + 1 và tính lại f(n)
- Solution từ UCS:
	+ Đặc điểm
		· Luôn tìm ra lời giải ngắn nhất nếu tồn tại, nhờ heuristic chính xác
		· Hiệu quả hơn BFS/UCS vì có định hướng nhờ hàm ước lượng
		· Phụ thuộc vào chất lượng heuristic — càng sát thực tế, thời gian chạy càng tốt
	
	+ Hiển thị trong chương trình
		· Hiển thị từng bước trong lời giải với STEP_DELAY = 300ms
		· Thời gian thực thi được in ra: "Time: x.xxxx seconds"
		· Các ô di chuyển được highlight để trực quan theo dõi đường đi

b. Thuật toán IDA*
* Hình ảnh gif mô tả thuật toán: (https://github.com/hnthach/BaiTapCaNhan_/blob/main/%E1%BA%A2nh_GIF/2.%20Informed%20Search/IDA_Star.gif?raw=true)
- Các thành phần chính
	+ Hàm heuristic (Manhattan Distance)
		· Sử dụng khoảng cách Manhattan để đánh giá chi phí còn lại
		· Bảo đảm tính admissible, giúp tìm được lời giải tối ưu
	+ Hàm tìm kiếm chính (ida_star_search)
		· Khởi tạo giới hạn (threshold) bằng heuristic của trạng thái bắt đầu
		· Lặp lại quá trình tìm kiếm với ngưỡng tăng dần cho đến khi tìm được lời giải
	+ Hàm tìm kiếm đệ quy (search)
		· g: chi phí từ trạng thái bắt đầu đến trạng thái hiện tại
		· f = g + h: tổng chi phí dự đoán
		· Nếu f > threshold: trả về chi phí f làm ngưỡng mới
		· Nếu tìm thấy trạng thái đích: trả về lời giải
		· Nếu không: duyệt các trạng thái kề bằng cách di chuyển ô trống
	+ Phần mở rộng trạng thái
		· Sinh các trạng thái mới từ các hướng di chuyển hợp lệ của ô trống
		· Tránh lặp lại trạng thái đã đi bằng cách kiểm tra trong path
		· Gọi đệ quy search với g + 1 và cập nhật ngưỡng nhỏ nhất nếu cần
	+ Vòng lặp chính
		· Cập nhật threshold nếu không tìm được lời giải ở lần lặp hiện tại
		· Lặp đến khi tìm được hoặc không thể tiếp tục (inf)
- Solution từ IDA*
	+ Đặc điểm
		· Tối ưu: luôn tìm đường đi ngắn nhất nếu heuristic đúng
		· Tiết kiệm bộ nhớ: chỉ lưu trạng thái trên đường đi hiện tại
		· Tìm kiếm lặp lại theo mức f, phù hợp cho không gian trạng thái lớn
	+ Hiển thị trong chương trình
		· Solution được mô phỏng từng bước với độ trễ STEP_DELAY = 300ms
		· Thời gian thực thi được in ra màn hình
		· Các ô thay đổi được highlight rõ ràng khi di chuyển

c. Greedy
* Hình ảnh gif mô tả thuật toán: (https://github.com/hnthach/BaiTapCaNhan_/blob/main/%E1%BA%A2nh_GIF/2.%20Informed%20Search/Greedy.gif?raw=true)
- Các thành phần chính
	+ Hàm heuristic (Manhattan Distance)
		. Ưu tiên mở rộng trạng thái có giá trị heuristic nhỏ nhất (gần goal nhất theo khoảng cách Manhattan)
		. Heuristic được dùng như tiêu chí duy nhất (không tính chi phí g thực tế như A*)
	+ Hàng đợi ưu tiên (Priority Queue)
		. Sắp xếp các trạng thái theo h(n) (heuristic)
		. Dùng heapq để chọn trạng thái "gần đích nhất" theo đánh giá của heuristic
	+ Tập hợp các trạng thái đã xét (Visited Set)
		. Tránh lặp lại các trạng thái đã mở rộng
		. Giúp cải thiện hiệu suất, tránh vòng lặp
	+ Hàm mở rộng trạng thái (Neighbor Function)
		. Tạo các trạng thái mới bằng cách di chuyển ô trống theo các hướng hợp lệ
		. Chỉ thêm vào queue nếu chưa được duyệt
- Solution từ Greedy
	+ Đặc điểm
		. Tập trung tối đa vào hướng đến goal, bỏ qua chi phí đã đi (g(n) không được tính)
		. Có thể không tìm ra đường đi ngắn nhất
		. Chạy nhanh và tiết kiệm bộ nhớ hơn A*, nhưng có thể đi sai hướng nếu heuristic không tốt
	+ Hiển thị trong chương trình
		. Hiển thị lời giải từng bước (nếu tìm được), sử dụng delay cố định (STEP_DELAY)
		. Thông tin thời gian thực thi được hiển thị
		. Các bước di chuyển được highlight nếu chương trình có hỗ trợ

2.2.2 Hình ảnh gif so sánh các thuật toán trong nhóm thuật toán tìm kiếm có thông tin
https://github.com/hnthach/BaiTapCaNhan_/blob/main/%E1%BA%A2nh_GIF/2.%20Informed%20Search/SoSanhHieuSuat_Informed%20Search.gif?raw=true

2.1.3 Nhận xét về hiệu suất các thuật toán
- A*
      + Ưu điểm
	        • Tìm được lời giải tối ưu (ngắn nhất) nếu tồn tại
	        • Hiệu quả khi sử dụng heuristic Manhattan Distance
	        • Thời gian chạy tốt trong hầu hết các trường hợp
      + Nhược điểm
	        • Tiêu tốn bộ nhớ do phải lưu trữ nhiều trạng thái
	        • Quá phức tạp khi kích thước của puzzle tăng lên

- UCS (Uniform Cost Search)
      + Ưu điểm
	        • Tìm được lời giải tối ưu như A*
	        • Đơn giản hơn A*
      + Nhược điểm
	        • Chậm hơn A* do không sử dụng heuristic
	        • Duyệt nhiều node không cần thiết

-  Greedy Best-First Search
      + Ưu điểm
	        • Tìm kiếm nhanh trong nhiều trường hợp
	        • Tập trung vào mục tiêu, giúp giảm thời gian tìm kiếm
      + Nhược điểm
	        • Không đảm bảo tìm được lời giải tối ưu
	        • Dễ rơi vào trạng thái local optima (tối ưu cục bộ)
```
2.3 Các thuật toán tìm kiếm nội bộ
```
2.3.1 Các thành phần chính của bài toán tìm kiếm và solution
a. Thuật toán simple hill climbing
- Các thành phần chính
	+ Hàm heuristic (Manhattan Distance)
		. Sử dụng khoảng cách Manhattan để đánh giá mức độ gần goal
		. Chỉ sử dụng h(n), không xét chi phí g(n) từ start → node như A*
	+ Hàm chính (simple_hill_climbing)
		. Bắt đầu từ trạng thái start, đánh giá heuristic ban đầu
		. Duyệt qua tối đa max_steps bước để tránh lặp vô hạn
		. Lưu đường đi trong path và theo dõi các trạng thái đã duyệt bằng visited
	+ Hàm mở rộng trạng thái (Neighbor Generation)
		. Tạo các trạng thái hợp lệ bằng cách di chuyển ô trống
		. Chỉ xét các trạng thái chưa được duyệt
		. Sắp xếp các trạng thái theo heuristic và chọn trạng thái tốt hơn hoặc bằng hiện tại
	+ Chiến lược leo đồi (Hill Climbing)
		. Nếu không tìm thấy trạng thái tốt hơn, có thể chọn ngẫu nhiên trong các trạng thái chưa thăm
		. Nếu không còn hướng nào cải thiện, kết thúc sớm (mắc kẹt tại local optima)
- Solution từ Simple Hill Climbing
	+ Đặc điểm
		. Nhanh và đơn giản, chỉ cần heuristic mà không cần hàng đợi ưu tiên
		. Có thể không tìm được lời giải nếu mắc kẹt tại đỉnh cục bộ (local optimum)
		. Không đảm bảo tìm ra đường đi ngắn nhất hoặc thậm chí không đến được goal
	+ Hiển thị trong chương trình
		. Đường đi (nếu tìm được) sẽ được hiển thị từng bước, với delay giữa các bước (STEP_DELAY)
		. Có thể hiển thị số bước thực hiện hoặc thời gian thực thi
		. Các trạng thái chuyển tiếp có thể được highlight để minh họa quá trình "leo đồi"

b. Thuật toán Steepest ascent hill climbing
*Hình ảnh gif mô tả thuật toán: https://github.com/hnthach/BaiTapCaNhan_/blob/main/%E1%BA%A2nh_GIF/3.%20Local%20Search/Steepest%20Hill.gif?raw=true
- Các thành phần chính
	+ Hàm heuristic (Manhattan Distance)
		. Sử dụng khoảng cách Manhattan để đo độ gần tới goal
		. Chỉ xét h(n), không tính g(n) như A*, UCS
	+ Hàm chính (steepest_hill_climbing)
		. Khởi tạo từ trạng thái start, lưu path và tập visited
		. Duyệt tối đa max_steps để giới hạn số lần lặp
		. Ở mỗi bước, tìm trạng thái hàng xóm có h(n) thấp nhất ("steepest descent")
	+ Hàm mở rộng trạng thái (Neighbor Generation)
		. Tạo các trạng thái hợp lệ bằng cách di chuyển ô trống
		. Chỉ xét các trạng thái chưa từng duyệt
		. Sắp xếp tất cả hàng xóm theo heuristic tăng dần
		. Lấy ra trạng thái có h thấp nhất và cập nhật nếu tốt hơn (hoặc ngang bằng)
	+ Chiến lược Leo đồi Dốc nhất (Steepest Ascent)
		. Nếu tìm thấy hàng xóm có heuristic tốt hơn → cập nhật
		. Nếu chỉ có hàng xóm ngang bằng → chọn ngẫu nhiên trong số đó
		. Nếu không còn hàng xóm chưa duyệt tốt hơn → có thể chọn ngẫu nhiên để thoát local optima
		. Nếu vẫn không có hướng đi mới → kết thúc (kẹt tại đỉnh cục bộ)
- Solution từ Steepest Hill Climbing
	+ Đặc điểm
		. Chọn hướng đi tốt nhất ở mỗi bước, không lưỡng lự như simple hill climbing
		. Có thể giúp tránh một số local optima hơn so với phiên bản đơn giản
		. Tuy nhiên vẫn có thể mắc kẹt nếu không có cải thiện rõ rệt
	+ Hiển thị trong chương trình
		. Hiển thị đường đi từng bước nếu tìm thấy solution
		. Có thể minh họa trạng thái bị kẹt khi không còn hướng đi tốt hơn
		. Thông tin số bước đã duyệt, thời gian thực thi có thể được in ra để đánh giá hiệu suất

c. Thuật toán Stochastic hill climbing
*Hình ảnh gif mô tả thuật toán: (https://github.com/hnthach/BaiTapCaNhan_/blob/main/%E1%BA%A2nh_GIF/3.%20Local%20Search/Stochastic%20hill.gif?raw=true)
- Các thành phần chính
	+ Hàm heuristic (Manhattan Distance)
		. Dùng để đánh giá mức độ gần với trạng thái đích
		. Chỉ sử dụng h(n), không tính đến chi phí thực như UCS hay A*
	+ Hàm chính (stochastic_hill_climbing)
		. Bắt đầu từ trạng thái start, lưu path và các trạng thái đã thăm visited
		. Lặp tối đa max_steps bước
		. Ở mỗi bước, tạo danh sách hàng xóm và phân loại thành: tốt hơn, ngang bằng, tệ hơn
	+ Hàm mở rộng trạng thái (Neighbor Generation)
		. Sinh ra tất cả các trạng thái có thể bằng cách di chuyển ô trống
		. Chỉ xét các trạng thái chưa từng thăm
		. Tính heuristic của từng trạng thái mới để phân nhóm
	+ Chiến lược Leo đồi Ngẫu nhiên (Stochastic Ascent)
		. Nếu có trạng thái tốt hơn, chọn ngẫu nhiên theo xác suất ưu tiên trạng thái cải thiện nhiều hơn
		. Nếu không có, có thể đi ngang (tức là trạng thái có heuristic bằng hiện tại)
		. Nếu bị kẹt quá nhiều bước (theo max_stuck), chấp nhận đi lùi (worsening) để thoát local optima
		. Điều này giúp thuật toán có tính linh hoạt hơn so với dạng hill climbing thông thường
- Solution từ Stochastic Hill Climbing
	+ Đặc điểm
		. Giảm nguy cơ mắc kẹt tại local optima bằng cách chọn bước đi ngẫu nhiên có xác suất
		. Có thể vượt local optima nhờ cơ chế “đi lùi có kiểm soát”
		. Mức độ khám phá cao hơn các thuật toán leo đồi đơn giản, đặc biệt với bài toán nhiều điểm kẹt như 8-puzzle
	+ Hiển thị trong chương trình
		. Có thể in ra từng trạng thái đã đi qua và thời điểm “chấp nhận đi lùi” để minh họa khả năng thoát kẹt
		. Đường đi thường dài hơn so với các thuật toán tối ưu như A*, nhưng khả năng tìm được lời giải trong nhiều tình huống kẹt cao hơn

d. Thuật toán Beam Search
*Hình ảnh gif mô tả thuật toán: (
- Các thành phần chính:
	+ Hàm heuristic (Manhattan Distance)
		. Dùng để đánh giá mức độ gần với trạng thái đích
		. Chỉ sử dụng h(n) – giống như Greedy, không xét chi phí thực tế g(n)
	+ Hàm chính (beam_search)
		. Khởi tạo current_states chứa trạng thái bắt đầu kèm giá trị heuristic và đường đi
		. Duyệt trong tối đa max_steps bước
		. Mỗi vòng lặp mở rộng tất cả trạng thái hiện tại → sinh trạng thái kế cận
		. Chọn beam_width trạng thái tốt nhất để tiếp tục (theo heuristic thấp nhất)
	+ Chiến lược tìm kiếm chùm (Beam Search)
		. Tại mỗi bước, chỉ giữ lại số lượng trạng thái giới hạn (beam_width)
		. Các trạng thái được chọn dựa theo giá trị heuristic tốt nhất, bỏ qua phần lớn không gian tìm kiếm
		. Do vậy, đây là thuật toán tìm kiếm theo chiều rộng có chọn lọc
	- Solution từ Beam Search
	+ Đặc điểm
		. Tập trung vào các trạng thái triển vọng nhất bằng cách chỉ giữ lại một số trạng thái tốt nhất tại mỗi bước (theo manhattan_distance)
		. Có thể bỏ qua lời giải tối ưu nếu nằm ngoài chùm, vì không duyệt toàn bộ không gian trạng thái
		. Hiệu quả cao về bộ nhớ hơn so với A* hay BFS vì chỉ giữ một số lượng trạng thái giới hạn (theo beam_width)
		. Dễ bị mắc kẹt nếu beam_width quá nhỏ hoặc không có trạng thái nào khả thi trong chùm
	+ Hiển thị trong chương trình
		. Lời giải là chuỗi các trạng thái từ start đến goal, hoặc trạng thái gần nhất trong chùm nếu không tìm thấy lời giải
		. Có thể in ra số bước đi, các trạng thái trong chùm tại mỗi bước để minh họa cơ chế chọn lọc
		. Thích hợp để chạy nhanh với kích thước chùm vừa phải, nhưng cần điều chỉnh beam_width hợp lý để đảm bảo không bỏ sót lời giải
```
