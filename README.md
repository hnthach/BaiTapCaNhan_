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
   
   2.1.1 Các thành phần chính của bài toán tìm kiếm và solution
   
   a. BFS
   
  ![BFS](https://github.com/user-attachments/assets/19ae5414-150e-4749-b0e3-2950a6d791e3)
   ```
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
   ```
   
   b. DFS
   
  ![DFS](https://github.com/user-attachments/assets/4828f44a-9ded-4c56-ae1a-e1a7c393ac7d)
```
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
		   . Thời gian thực thi: Phụ thuộc vào độ sâu tối đa max_depth và cấu trúc cây trạng thái; độ phức tạp trong trường hợp xấu là O(b^d), với b là branching factor và d là độ sâu lời giải
```
   c. IDDFS  
   
   ![IDDFS](https://github.com/user-attachments/assets/261dc269-ba4b-482a-98be-3a2866c9f5d6)
```
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
   ```
   d. UCS  

   ![UCS](https://github.com/user-attachments/assets/0f16ed88-fe7b-4781-9b2a-520a45efb57a)
```
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
```
   2.1.2 Hình ảnh so sánh hiệu suất các thuật toán trong nhóm thuật toán tìm kiếm không có thông tin  

   
   ![SoSanhHieuXuat_Uninformed Search](https://github.com/user-attachments/assets/d5c9bb95-066e-43c7-9cc0-23927365d460)  

   ![image](https://github.com/user-attachments/assets/9e21d9a2-19a1-4d22-bd67-10760da9d877)

   
   2.1.3 Nhận xét về hiệu suất các thuật toán
   ```
	   - BFS đảm bảo tìm ra lời giải ngắn nhất về số bước, nhưng tiêu tốn rất nhiều bộ nhớ do phải lưu toàn bộ trạng thái ở từng mức sâu. Với bài toán như 8-puzzle, BFS dễ bị giới hạn tài nguyên khi độ sâu tăng.
	   - DFS sử dụng ít bộ nhớ hơn do đi sâu theo nhánh, nhưng dễ bị lặp vô hạn và không đảm bảo tìm được lời giải ngắn nhất. Giới hạn độ sâu có thể giúp tránh lặp nhưng có nguy cơ bỏ sót lời giải.
	   - IDDFS khắc phục cả nhược điểm của BFS và DFS: tiết kiệm bộ nhớ, đồng thời vẫn tìm được lời giải ngắn nhất nhờ việc lặp DFS với độ sâu tăng dần.
	   - UCS tối ưu về chi phí thay vì độ dài đường đi. Khi chi phí mỗi bước giống nhau, UCS tương đương BFS. Tuy nhiên, UCS tiêu tốn bộ nhớ lớn do dùng hàng đợi ưu tiên để xử lý trạng thái theo tổng chi phí thấp nhất.
   
   ```
2.2 Các thuật toán tìm kiếm có thông tin (Informed Search)  

2.2.1 Các thành phần chính của bài toán tìm kiếm và solution  

a. Thuật toán A*  

![A_Star](https://github.com/user-attachments/assets/99e7a577-b3d4-4e72-9348-46a65ee96d7a)

```
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
```
b. Thuật toán IDA*  

![IDA_Star](https://github.com/user-attachments/assets/0673cbd7-0f31-4c6d-be75-ee44b0ea067f)
```
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
```
c. Greedy  

![Greedy](https://github.com/user-attachments/assets/8439d686-9224-441d-8582-5a84db342d78)
```
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
```
2.2.2 Hình ảnh gif so sánh các thuật toán trong nhóm thuật toán tìm kiếm có thông tin  

![SoSanhHieuSuat_Informed Search](https://github.com/user-attachments/assets/fcc6a19b-6d18-45fb-a0e9-80689435dae8)


2.2.3 Nhận xét về hiệu suất các thuật toán
```
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

2.3.1 Các thành phần chính của bài toán tìm kiếm và solution  

a. Thuật toán simple hill climbing  

![Simple_Hill](https://github.com/user-attachments/assets/26664efb-846a-45ee-84ac-67a06333a47b)

=> Trong quá trình sắp xếp, thuật toán đã rơi vào điểm cực trị cục bộ (local optimum) tại bước di chuyển số 2, khiến nó không thể tiếp tục tìm ra lời giải.
```
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
```
b. Thuật toán Steepest ascent hill climbing  

![Steepest Hill](https://github.com/user-attachments/assets/f26ff33b-66cd-42ed-985f-f391235e13e6)
```
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
=> Trong quá trình sắp xếp, thuật toán có thể rơi vào điểm cực trị cục bộ (local optimum) , khiến nó không thể tiếp tục tìm ra lời giải. 
```
c. Thuật toán Stochastic hill climbing  

![Stochastic hill](https://github.com/user-attachments/assets/ac5f227f-46f2-48bb-bc5d-45ea308a8f42)
```
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
```
d. Thuật toán Beam Search  

![Beam Search](https://github.com/user-attachments/assets/966caf38-ab3a-4fee-8227-38a0e17f14a8)
```
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
e. Thuật toán Simulated Annealing

![Simulated Annealing](https://github.com/user-attachments/assets/29fc79c0-89db-40eb-8903-f446df85add2)

```
- Các thành phần chính
	+ Hàm heuristic (Manhattan Distance)
		. Dùng để đánh giá độ gần của trạng thái hiện tại với trạng thái đích
		. Chỉ dùng h(n) nên không xét đến chi phí thực tế như UCS hay A*
	+ Hàm chính (simulated_annealing)
		. Khởi tạo từ start, thiết lập initial_temp (nhiệt độ ban đầu), cooling_rate (tốc độ làm nguội)
		. Duy trì path và cập nhật theo từng trạng thái đã chọn
		. Lặp tối đa max_steps bước hoặc dừng sớm nếu nhiệt độ xuống quá thấp
	+ Hàm mở rộng trạng thái (Neighbor Generation)
		. Sinh ra tất cả các trạng thái hợp lệ bằng cách di chuyển ô trống
		. Với mỗi trạng thái sinh ra, tính heuristic để quyết định khả năng chấp nhận
	+ Chiến lược Mô phỏng luyện kim (Simulated Annealing)
		. Luôn chấp nhận trạng thái tốt hơn
		. Có thể chấp nhận trạng thái tệ hơn với xác suất giảm dần theo thời gian (phụ thuộc vào nhiệt độ temp)
		. Xác suất chấp nhận bước đi xấu hơn được tính theo công thức: P = exp((current_h - new_h) / temp)
		. Khi temp giảm dần, hệ thống sẽ trở nên bảo thủ hơn (ít chấp nhận trạng thái tệ)
- Solution từ Simulated Annealing
	+ Đặc điểm
		. Có khả năng thoát khỏi local optima nhờ chấp nhận trạng thái kém hơn một cách có kiểm soát
		. Cân bằng giữa khai phá (exploration) và khai thác (exploitation) qua quá trình làm nguội
		. Phù hợp với bài toán có không gian trạng thái phức tạp và nhiều điểm mắc kẹt
		. Không đảm bảo tối ưu nhưng thường tìm ra lời giải tốt nếu cấu hình tham số hợp lý (initial_temp, cooling_rate)
	+ Hiển thị trong chương trình
		. Có thể hiển thị biểu đồ nhiệt độ theo thời gian, hoặc số lần chấp nhận bước đi tệ hơn
		. In ra trạng thái khi thuật toán "đi lùi" để minh họa tính linh hoạt
		. Có thể so sánh hiệu suất với Hill Climbing để thấy rõ vai trò của cơ chế “chấp nhận sai lầm có kiểm soát”
```
f. Thuật toán Genetic Algorithm

![Genetic Algorithm](https://github.com/user-attachments/assets/61ab014c-4c1a-4cb9-98a2-e94bbf120d0d)

```
- Các thành phần chính
	+ Hàm heuristic (Manhattan Distance)
		・Dùng để đánh giá độ gần của trạng thái cuối cùng trong đường đi của một cá thể so với trạng thái đích (goal)
		・Hàm fitness trả về giá trị âm của khoảng cách để dễ dàng tối đa hóa (càng gần đích, giá trị càng lớn)
	+ Hàm chính (genetic_algorithm)
		・Khởi tạo quần thể gồm nhiều cá thể bằng cách thực hiện các bước đi ngẫu nhiên từ start
		・Mỗi cá thể là một dãy các trạng thái (đường đi), không phải chỉ là 1 cấu hình
		・Duy trì vòng lặp qua tối đa max_generations, mỗi thế hệ đều tiến hành đánh giá, chọn lọc, lai ghép và đột biến
	+ Hàm sinh cá thể (Individual Generation)
		・Tạo đường đi ngẫu nhiên từ trạng thái bắt đầu, với số bước di chuyển từ 5–30
		・Mỗi bước sinh một trạng thái mới bằng cách di chuyển ô trống hợp lệ
	+ Đánh giá độ thích nghi (Fitness Evaluation)
		・Fitness được tính theo khoảng cách Manhattan của trạng thái cuối cùng của đường đi
		・Dùng để xếp hạng và chọn lọc các cá thể tốt hơn qua từng thế hệ
	+ Chiến lược di truyền (Genetic Strategy)
		・Chọn lọc: giữ lại 50% cá thể có độ thích nghi cao nhất
		・Lai ghép (crossover): kết hợp hai cha mẹ bằng cách cắt đường đi tại một điểm ngẫu nhiên
		・Đột biến (mutation): với xác suất mutation_rate, thêm một bước đi ngẫu nhiên để giữ tính đa dạng và thoát local optima
		・Lặp lại cho đến khi tạo đủ population_size cá thể mới

- Solution từ Genetic Algorithm
+ Đặc điểm
	・Là thuật toán tìm kiếm ngẫu nhiên dựa trên tiến hóa sinh học
	・Có khả năng tìm kiếm song song nhiều hướng giải khác nhau nhờ vào quần thể
	・Không đảm bảo tìm ra lời giải tối ưu, nhưng dễ mở rộng, dễ kết hợp với heuristic khác
	・Phù hợp với các bài toán có không gian trạng thái lớn và độ phức tạp cao
+ Hiển thị trong chương trình
	・Có thể in ra trạng thái cá thể tốt nhất mỗi thế hệ (kèm fitness)
	・Minh họa sự khác biệt giữa thế hệ cha và con sau crossover/mutation
	・Biểu đồ biểu diễn tiến trình cải thiện fitness qua các thế hệ
```

2.3.2 Hình ảnh gif so sánh các thuật toán trong nhóm thuật toán tìm kiếm nội bộ  

![SoSanhHieuSuat_Local Search](https://github.com/user-attachments/assets/78a410ad-e0d9-4a26-a5dd-9db641f517d0)

2.3.3 Nhận xét về hiệu suất các thuật toán

```
- Simple Hill Climbing
	+ Ưu điểm
		• Dễ cài đặt, trực tiếp cải thiện trạng thái hiện tại
		• Tốc độ nhanh, tiêu thụ bộ nhớ ít
	+ Nhược điểm
		• Dễ bị kẹt ở local optimum
		• Không lùi lại hay thử lựa chọn thay thế
		• Không đảm bảo tìm được lời giải
- Steepest-Ascent Hill Climbing
	+ Ưu điểm
		• Tìm bước đi tốt nhất tại mỗi lượt, tăng cơ hội cải thiện
		• Có thể hiệu quả hơn Simple Hill Climbing trong không gian trạng thái mịn
	+ Nhược điểm
		• Vẫn dễ kẹt tại local optimum hoặc plateau (vùng bằng phẳng)
		• Mỗi bước cần đánh giá toàn bộ hàng xóm → chậm hơn
- Stochastic Hill Climbing
	+ Ưu điểm
		• Chọn ngẫu nhiên hàng xóm tốt → tránh bị mắc kẹt sớm
		• Nhanh và tiết kiệm bộ nhớ
	+ Nhược điểm
		• Không đảm bảo tìm lời giải
		• Hiệu quả không ổn định, phụ thuộc may mắn
		• Có thể dừng ở local optima nếu hàng xóm hạn chế
- Beam Search
	+ Ưu điểm
		• Kiểm soát bộ nhớ bằng beam_width, tiết kiệm so với A*
		• Tốc độ nhanh nếu beam nhỏ
	+ Nhược điểm
		• Có thể bỏ qua lời giải đúng nếu beam quá hẹp
		• Không đảm bảo tối ưu
		• Nhạy cảm với chất lượng heuristic
- Simulated Annealing
	+ Ưu điểm
		• Có khả năng thoát local optima bằng cách chấp nhận bước đi xấu tạm thời
		• Phù hợp cho không gian trạng thái phức tạp
	+ Nhược điểm
		• Không ổn định: kết quả thay đổi nếu chạy lại
		• Cần tinh chỉnh nhiều tham số (nhiệt độ, tốc độ làm nguội)
		• Có thể không tìm ra lời giải nếu "lạnh" quá nhanh

- Genetic Algorithm
	+ Ưu điểm
		• Khả năng tìm kiếm đa dạng nhờ quần thể và đột biến
		• Tốt trong việc tránh local optima
		• Có thể tiếp cận lời giải nếu cấu hình đúng
	+ Nhược điểm
		• Cần thời gian hội tụ dài
		• Hiệu quả phụ thuộc vào kích thước quần thể, tỉ lệ lai ghép, đột biến
		• Không đảm bảo lời giải đúng
```
2.4 Các thuật toán tìm kiếm trong môi trường phức tạp  

2.4.1 Các thành phần chính của bài toán tìm kiếm và solution  

a. Thuật toán Nondeterministic Search
```
- Các thành phần chính
       + Hàm heuristic kỳ vọng (expected_heuristic)
	         . Mục đích: Điều chỉnh heuristic thông thường để tính đến yếu tố không xác định
	         . Cách tính: Nhân khoảng cách Manhattan với hệ số 1/xác_suất_thành_công
	         . Ý nghĩa: Khi xác suất thành công thấp, heuristic giá trị cao hơn để phản ánh độ khó
        + Cấu trúc dữ liệu và khởi tạo
	          . Open set: Hàng đợi ưu tiên lưu (f_score, cost, state, path)
	          . Visited set: Tập hợp các trạng thái đã xét để tránh lặp
        + Vòng lặp chính
	          . Lấy trạng thái có f_score nhỏ nhất từ open set
	          . Kiểm tra điều kiện dừng khi gặp goal state
	          . Bỏ qua các trạng thái đã xét
        + Xử lý hành động không xác định
	          . Tìm các trạng thái kề có thể có
	          . Trong phiên bản đơn giản này, chỉ xét trạng thái mong muốn (không xét các trạng thái lỗi)
  - Phân tích solution
        + Ưu điểm
	          . Kế thừa ưu điểm của A*: Đảm bảo tìm được lời giải tối ưu nếu tồn tại
	          . Xử lý không xác định: Heuristic điều chỉnh phản ánh độ không chắc chắn
	          . Hiệu quả: Vẫn duy trì được tính hiệu quả của A* trong môi trường không xác định
        + Nhược điểm
	          . Phiên bản đơn giản hóa: Chỉ xét trạng thái mong muốn, không mô hình hóa đầy đủ các kết quả có thể có
	          . Heuristic đơn giản: Chỉ nhân hệ số cố định, chưa phản ánh chính xác xác suất các trạng thái khác nhau
```
b. Thuật toán Partial Observation
```
  - Các thành phần chính
        + Khởi tạo quan sát một phần
	          . Mục đích: Tạo trạng thái quan sát ban đầu với một số ô bị ẩn
	          . Cách hoạt động: Chọn ngẫu nhiên num_hidden ô để ẩn, chỉ giữ lại giá trị các ô hiển thị
        + Belief States (Trạng thái niềm tin)
	          . Định nghĩa: Tập hợp tất cả các trạng thái có thể phù hợp với quan sát hiện tại
	          . Trong triển khai đơn giản: Chỉ sử dụng trạng thái thực (để minh họa)
	          . Triển khai đầy đủ: Cần sinh tất cả trạng thái có thể khớp với các ô đã quan sát
        + Vòng lặp tìm kiếm chính
	          . Vòng lặp tìm kiếm chính
	          . Mỗi bước: Chọn hành động, thực hiện di chuyển, cập nhật thông tin
        + Cập nhật quan sát
	          . Quy tắc: Ô trống (0) luôn được tiết lộ khi nó di chuyển vào vị trí bị ẩn
	          . Mục đích: Giảm dần số ô bị ẩn khi puzzle được giải
        + Cập nhật Belief States
	          . Chức năng: Lọc các trạng thái trong belief states để chỉ giữ lại những cái phù hợp với quan sát mới
	          . Triển khai đầy đủ: Cần kiểm tra tính nhất quán của mỗi trạng thái với observation
- Phân tích solution
        + Ưu điểm
	          . Mô phỏng quan sát không đầy đủ: Giải quyết bài toán thực tế khi không thấy toàn bộ trạng thái
	          . Tiếp cận Belief State: Phù hợp với lý thuyết POMDP (Partially Observable MDP)
	          . Cơ chế tiết lộ thông tin: Tự động phát hiện ô trống khi nó di chuyển vào vị trí ẩn
        + Nhược điểm
	          . Triển khai đơn giản hóa: Chưa thực sự quản lý belief states đầy đủ
	          . Chiến lược chọn hành động ngẫu nhiên: Không tối ưu, có thể dẫn đến hiệu suất thấp
	          . Thiếu cơ chế xử lý khi belief states rỗng: Không xử lý trường hợp không có trạng thái nào phù hợp  
Giải pháp Partial Observation Search cung cấp cách tiếp cận hợp lý cho bài toán 8-puzzle với thông tin không đầy đủ. Phiên bản hiện tại là một khung cơ bản tốt
```
c. Thuật toán tìm kiếm không quan sát
```
- Các thành phần chính
	+ Mô hình tìm kiếm không quan sát
		. Thuật toán mô phỏng một tác nhân không có khả năng quan sát trạng thái hiện tại sau khi thực hiện hành động, do đó phải ghi nhớ tất cả các trạng thái đã đi qua để tránh đi vòng lặp lại.
		. Đây là một dạng tìm kiếm ngẫu nhiên có ghi nhớ, không có chiến lược tối ưu hay heuristic cụ thể.
		. Thuật toán hoạt động theo một logic rất đơn giản: di chuyển ngẫu nhiên nhưng tránh các trạng thái đã thăm. Nếu bị bế tắc (không còn nước đi mới), thuật toán quay lui (backtrack).
	+ Cấu trúc hàm no_observation_search(start, goal)
	.  Đầu vào:
		.  start: trạng thái bắt đầu
		. goal: trạng thái mục tiêu
		. max_steps: số bước tối đa (tránh lặp vô hạn)
	. Khởi tạo:
		. current_state: trạng thái hiện tại
		. path: danh sách các trạng thái đã đi qua
		. visited: tập hợp các trạng thái đã đến, để tránh lặp lại
	+ Vòng lặp tìm kiếm
	.  Ở mỗi bước:
		. Kiểm tra nếu current_state == goal thì trả về path
		. Tìm tất cả các hành động (dịch chuyển ô trống) có thể từ trạng thái hiện tại
		. Lọc ra các hành động chưa từng tạo ra trạng thái đã thăm
		. Nếu không còn hành động hợp lệ nào:
		. Quay lui một bước (pop khỏi path), cập nhật lại trạng thái hiện tại
	. Nếu còn:
		. Chọn một hành động ngẫu nhiên, thực hiện, cập nhật current_state, thêm vào path và visited
	+ Kết thúc
	. Thuật toán dừng nếu:
		. Tìm được trạng thái đích
		. Vượt quá max_steps
		. Không thể tiếp tục đi thêm và không còn đường để quay lui
- Solution từ tìm kiếm không quan sát
	+ Đặc điểm
		. Mô phỏng tốt một môi trường không có cảm biến hay quan sát, như robot hoạt động "mù" trong mê cung
		. Dễ cài đặt, không cần heuristic hay hàm đánh giá
		. Chiến lược đơn giản: chọn ngẫu nhiên, tránh trùng, backtrack nếu bị kẹt
		. Hiệu quả thấp, dễ rơi vào vòng lặp, mất nhiều bước và không đảm bảo tìm ra lời giải nếu max_steps không đủ lớn
		. Tuy nhiên, có thể sử dụng như baseline để so sánh với các thuật toán có chiến lược tốt hơn (BFS, A*, Hill Climbing...)
	+ Hiển thị trong chương trình
		. Trả về đường đi đã khám phá
		. Có thể hiển thị số bước đã đi, số trạng thái đã thăm
		. Có thể đánh giá: mất bao nhiêu bước, tỷ lệ thành công, tốc độ tìm ra lời giải

```
2.5 Các thuật toán tìm kiếm Constraint Satisfaction Problems (CSPs)  

a. Thuật toán Backtracking

![Backtracking](https://github.com/user-attachments/assets/48fd7226-40e5-434c-91b7-aa6c2022776c)

```
- Các thành phần chính
	+ Không gian tìm kiếm và trạng thái
		. Trạng thái ban đầu current_state là ma trận 3x3 chứa toàn số 0 (chưa gán).
		. Tập biến variables gồm tất cả các vị trí ô trên lưới (từ (0,0) đến (2,2)).
		. Mỗi biến có domain là tập {1, 2, ..., 8} – các giá trị có thể gán.
	+ Hàm kiểm tra ràng buộc: is_valid()
		. Đảm bảo giá trị vừa gán không trùng:
		. Trong cùng hàng.
		. Trong cùng cột.
		. Với các giá trị đã dùng ở các hàng trước đó (ràng buộc toàn cục).
		. Đây là bước đảm bảo tính hợp lệ cục bộ và tương thích tổng thể của lời giải tại thời điểm hiện tại.
	+ Hàm hiển thị trạng thái: draw_state_with_current_var()
		. Mỗi lần gán hoặc backtrack, trạng thái được hiển thị trực quan bằng Pygame.
		. Ô đang xét được tô màu khác (vàng nhạt) và hiển thị dấu "?" nếu chưa gán.
		. Góp phần minh họa rõ quá trình tìm lời giải từng bước một, phục vụ cho mục đích trực quan hóa thuật toán.
	+ Thuật toán chính: backtrack()
		. Là một hàm đệ quy thực hiện quá trình:
		. Gán thử từng giá trị hợp lệ cho ô hiện tại.
		. Hiển thị trạng thái sau mỗi lần gán.
		. Kiểm tra ràng buộc, nếu hợp lệ thì tiếp tục với biến kế tiếp.
		. Nếu không hợp lệ hoặc không dẫn tới lời giải, quay lui và thử giá trị khác (backtracking).
	+ Quá trình kết thúc khi:
		. Tìm được lời giải phù hợp với goal, trả về True.
		. Hoặc đã thử hết mà không đạt goal, trả về False.
- Solution từ thuật toán Backtracking
	+ Đặc điểm
	. Ưu điểm:
		. Có khả năng tìm toàn bộ không gian nghiệm, đảm bảo tìm ra lời giải (nếu có).
		. Dễ kiểm soát ràng buộc phức tạp nhờ kiểm tra điều kiện trước khi đi tiếp.
		. Rất phù hợp với các bài toán dạng Constraint Satisfaction Problem (CSP).
	. Nhược điểm:
		. Tốc độ chậm hơn so với các giải pháp heuristic vì phải thử nhiều tổ hợp.
		. Hiệu suất thấp nếu không có chiến lược cải tiến (như forward checking, MRV, ...).
		. Hiển thị trong chương trình
		. Trạng thái lưới được vẽ bằng Pygame sau mỗi bước gán hoặc quay lui.
		. Ô đang xét được tô màu và đánh dấu rõ ràng, dễ theo dõi quá trình giải.
		. Khi tìm được lời giải:
		. Trạng thái cuối được nhấp nháy để nhấn mạnh thành công.
		. Hỗ trợ việc học và trình bày thuật toán một cách trực quan và sinh động.
```
b. Thuật toán Backtracking With Forward Checking

![Backtracking_forward checking](https://github.com/user-attachments/assets/46a293cb-1a4e-4ff2-8b9f-6d30f6bd46d3)


```
- Các thành phần chính
	+ Không gian tìm kiếm và trạng thái
		. current_state: ma trận 3x3 khởi tạo toàn số 0, đại diện cho trạng thái hiện tại của bài toán.
		. variables: danh sách các vị trí trên lưới từ (0,0) đến (2,2), là các biến cần gán giá trị.
		. domains: mỗi biến có tập giá trị khả dĩ là {1, 2, ..., 8}, tức là các số có thể xuất hiện trong lưới.
	+ Hàm kiểm tra ràng buộc: is_valid()
		. Kiểm tra xem giá trị vừa gán có vi phạm ràng buộc không:
		. Không trùng với các giá trị cùng hàng.
		. Không trùng với các giá trị cùng cột.
		. Không trùng với giá trị đã xuất hiện ở các hàng phía trên (đảm bảo không trùng toàn cục).
		. Đây là bước xác thực tính hợp lệ cục bộ và toàn cục để đảm bảo lời giải từng bước là hợp lệ.
	+ Hàm hiển thị trạng thái: draw_state_with_current_var()
		. Cập nhật giao diện mỗi khi gán giá trị hoặc backtrack.
		. Ô hiện tại được tô vàng nhạt và hiển thị dấu "?" nếu chưa gán giá trị.
		. Trạng thái lưới được vẽ bằng thư viện Pygame, giúp minh họa trực quan tiến trình giải bài toán.
	+ Hàm forward checking: forward_check()
		. Khi gán một giá trị, thuật toán sẽ kiểm tra tác động của nó lên các biến chưa gán:
		. Cập nhật lại domain của các biến trong hàng, cột và các hàng phía trên.
		. Nếu phát hiện có biến nào bị rỗng domain → quay lui ngay (cắt tỉa nhánh sai).
		. Giúp loại bỏ sớm các nhánh không khả thi, tránh mất thời gian backtrack sau này.
	+ Thuật toán chính: backtrack()
		. Là hàm đệ quy thực hiện:
		. Duyệt qua từng biến theo thứ tự.
		. Thử từng giá trị trong domain.
		. Hiển thị trạng thái sau mỗi bước gán.
		. Kiểm tra ràng buộc và thực hiện forward checking.
		. Nếu hợp lệ, tiếp tục đệ quy với biến tiếp theo.
		. Nếu không thành công, quay lui và thử giá trị khác.
	+ Quá trình kết thúc khi:
		. Tìm được lời giải khớp với goal → trả về True.
		. Hoặc đã thử hết các khả năng mà không thành công → trả về False.
- Solution từ thuật toán Backtracking Forward Checking
+ Đặc điểm
	. Ưu điểm:
		. Có khả năng tìm được lời giải chính xác nếu tồn tại, nhờ tìm kiếm toàn bộ không gian nghiệm.
		. Forward checking giúp cắt tỉa nhánh sai sớm, tăng hiệu suất.
		. Phù hợp với các bài toán ràng buộc chặt chẽ, như Sudoku, Latin Square, hay bài toán phân công.
	. Nhược điểm:
		. Dù có cải tiến forward checking, nhưng vẫn có thể tốn thời gian khi không có thêm chiến lược heuristic (ví dụ: MRV, Degree).
		. Chưa sử dụng kỹ thuật sắp xếp biến hay thứ tự giá trị tối ưu.
	. Hiển thị trong chương trình
		. Giao diện Pygame minh họa trực quan quá trình giải:
		. Các bước gán giá trị và backtrack được hiển thị rõ ràng.
		. Ô đang xét được tô màu và đánh dấu, dễ quan sát.
		. Khi tìm được lời giải:
			. Lưới nhấp nháy 10 lần để nhấn mạnh thành công.
			. Giúp người học dễ hiểu và theo dõi thuật toán từng bước.


```
2.5.2 Hình ảnh gif so sánh các thuật toán trong nhóm thuật toán tìm kiếm nội bộ

![SoSanhHieuSuat_CSP](https://github.com/user-attachments/assets/7d096717-db3c-430d-a8a5-d5475a600968)

2.5.3 Nhận xét về hiệu suất các thuật toán
```
- Thuật toán Backtracking
	+ Ưu điểm:
		. Đơn giản, dễ cài đặt, dễ hiểu.
		. Tìm kiếm toàn diện trong không gian nghiệm, đảm bảo tìm được lời giải (nếu có).
	+ Nhược điểm:
		. Tốc độ chậm khi không có cơ chế cắt tỉa thông minh.
		. Có thể thử nhiều tổ hợp không hợp lệ trước khi phát hiện sai và quay lui.
		. Không phát hiện sớm các ràng buộc bất khả thi → tốn thời gian không cần thiết.
- Thuật toán Backtracking with Forward Checking
	+ Ưu điểm:
		. Tăng hiệu suất rõ rệt bằng cách loại bỏ sớm các giá trị không hợp lệ khỏi domain của các biến chưa gán.
		. Hạn chế số lần quay lui, đặc biệt hiệu quả trong các bài toán có ràng buộc chặt chẽ.
		. Giảm số bước thử nghiệm so với backtracking đơn thuần.
	+ Nhược điểm:
		. Cần thêm xử lý để duy trì và cập nhật domain → tăng độ phức tạp khi cài đặt.
		. Vẫn chưa tận dụng tối ưu nếu không kết hợp thêm các chiến lược heuristic như MRV (Minimum Remaining Values) hoặc Degree Heuristic.
```

2.6 Các thuật toán tìm kiếm Reinforcement Learning

a. Thuật toán Q – Learning

![Q – Learning](https://github.com/user-attachments/assets/115e9ba9-2323-45e4-b175-5d7a90da8f12)

```
- Các thành phần chính
	+ Mô hình Q-Learning
		• Q-Learning là một thuật toán học tăng cường (reinforcement learning).
		• Mục tiêu là học một hàm Q(s, a) cho biết giá trị kỳ vọng nếu thực hiện hành động a tại trạng thái s, theo công thức:
		𝑄(𝑠,𝑎)=𝑄(𝑠,𝑎)+𝛼⋅(𝑟+𝛾⋅max⁡𝑎′𝑄(𝑠′,𝑎′)−𝑄(𝑠,𝑎))Q(s,a)=Q(s,a)+α⋅(r+γ⋅ a ′max Q(s ′ ,a ′ )−Q(s,a))
		• Trong đó:
			• α là learning rate
			• γ là discount factor
			• r là phần thưởng (reward)
			• ε là xác suất thăm dò ngẫu nhiên (exploration rate)
	+ Cấu trúc lớp QLearningSolver
		• Khởi tạo với các tham số cơ bản (alpha, gamma, epsilon, episodes)
		• Dữ liệu học được lưu trong Q-table, là một dictionary {state: {action: value}}
		• Trạng thái state là cấu hình 8-puzzle, hành động action là một bước di chuyển hợp lệ của ô trống
	+ Hàm get_actions(state)
		• Trả về danh sách các hành động hợp lệ từ trạng thái hiện tại
		• Mỗi hành động là một tuple (r1, c1, r2, c2), đại diện cho việc di chuyển ô trống
	+  Hàm choose_action(state)
		• Chiến lược ε-greedy:
		• Với xác suất ε, chọn hành động ngẫu nhiên (exploration)
		• Ngược lại, chọn hành động tốt nhất theo Q-table (exploitation)
	+ Hàm update_q_table(state, action, reward, next_state)
		• Cập nhật giá trị Q cho một cặp trạng thái – hành động theo công thức Q-learning
	+ Hàm solve(start, goal)
		• Chạy Q-learning trong episodes vòng lặp
		• Mỗi vòng là một episode: bắt đầu từ start, chọn hành động, cập nhật Q-table cho đến khi đạt goal
		• Phần thưởng:
			• -1 cho mỗi bước
			• +100 nếu đạt được trạng thái goal
	+ Trả về kết quả
		• Sau khi huấn luyện, Q-table có thể dùng để sinh đường đi tốt nhất từ start đến goal
		• Sử dụng lại choose_action() để lần theo đường đi học được
- Solution từ Q-Learning
	+ Đặc điểm
		• Là một phương pháp tự học thông qua tương tác với môi trường
		• Khác với thuật toán tìm kiếm truyền thống: Q-Learning không cần biết trước mô hình (model-free)
		• Có khả năng ghi nhớ và cải thiện theo thời gian, học tốt nếu số lần lặp đủ lớn
		• Tuy nhiên, hiệu quả phụ thuộc lớn vào cách biểu diễn trạng thái, hàm thưởng, và số vòng học
	+ Hiển thị trong chương trình
		• In tổng phần thưởng của mỗi tập huấn luyện (episode)
		• Sau huấn luyện, in ra đường đi từ trạng thái bắt đầu đến đích theo Q-table
		• Có thể mở rộng thêm biểu đồ reward theo episode để theo dõi quá trình học
```
