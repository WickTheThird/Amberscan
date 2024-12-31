<script>
	// @ts-nocheck
	import '../app.css';
</script>

<slot />

<!-- component -->
<div class="flex bg-blue-500ray-50 z-0 overscroll-y-none w-full justify-center">
	<div class="py-10 sm:py-16 block lg:py-24 relative bg-opacity-50 z-40">
		<div
			class="relative mx-auto h-full px-4 pb-20 md:pb-10 sm:max-w-xl md:max-w-full md:px-24 lg:max-w-screen-xl lg:px-8"
		>
			<div class=" absolute top-0 -right-1/4 z-0 opacity-10">
				<svg
					width="800px"
					height="800px"
					viewBox="0 0 24 24"
					class="w-96 z-0 h-full object-fill fill-g text-g"
					fill="none"
					xmlns="http://www.w3.org/2000/svg"
				>
					<path
						fill-rule="evenodd"
						clip-rule="evenodd"
						d="M12 6C12 5.44772 11.5523 5 11 5C10.4477 5 10 5.44772 10 6V16C10 16.5523 10.4477 17 11 17C11.5523 17 12 16.5523 12 16V6ZM9 9C9 8.44772 8.55228 8 8 8C7.44772 8 7 8.44772 7 9V16C7 16.5523 7.44772 17 8 17C8.55228 17 9 16.5523 9 16V9ZM15 9C15 8.44772 14.5523 8 14 8C13.4477 8 13 8.44772 13 9V16C13 16.5523 13.4477 17 14 17C14.5523 17 15 16.5523 15 16V9ZM18 13C18 12.4477 17.5523 12 17 12C16.4477 12 16 12.4477 16 13V16C16 16.5523 16.4477 17 17 17C17.5523 17 18 16.5523 18 16V13ZM6 15C6 14.4477 5.55228 14 5 14C4.44772 14 4 14.4477 4 15V16C4 16.5523 4.44772 17 5 17C5.55228 17 6 16.5523 6 16V15ZM21 15C21 14.4477 20.5523 14 20 14C19.4477 14 19 14.4477 19 15V16C19 16.5523 19.4477 17 20 17C20.5523 17 21 16.5523 21 16V15ZM4 18C3.44772 18 3 18.4477 3 19C3 19.5523 3.44772 20 4 20H21C21.5523 20 22 19.5523 22 19C22 18.4477 21.5523 18 21 18H4Z"
					/>
				</svg>
			</div>

			<div class="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8 relative">
				<!-- <dv class="max-w-xl mx-auto text-center">
					<div class="inline-flex px-4 py-1.5 mx-auto rounded-full">
						<p class="text-4xl font-semibold tracking-widest text-g uppercase">Actions:</p>
					</div>
					<p class="mt-4 text-base leading-relaxed text-gray-600 group-hover:text-white">
						You can also search for specific data utilising pre specified time periods in the following format <b>dd/mm/yyyy - dd/mm/yyyy</b>.<br>
						You can specify the client name before or after the time period.
					</p>
				</dv> -->
				<div class="grid grid-cols-1 gap-2 mt-12 sm:grid-cols-2 lg:mt-20">
					<a
						href="#1"
						class="transition-all duration-1000 bg-white hover:bg-blue-500 hover:shadow-xl m-2 p-4 relative z-40 group rounded-lg"
					>
						<div
							class=" absolute bg-blue-500/50 top-0 left-0 w-24 h-1 z-30 transition-all duration-200 group-hover:bg-white group-hover:w-1/2"
						></div>
						<div class="py-2 px-9 relative">
							<svg
								class="w-16 h-16 text-gray-400 group-hover:text-white"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="1.5"
									d="M12 6v6m0 0v6m0-6h6m-6 0H6"
								></path>
							</svg>
							<h3 class="mt-8 text-lg font-semibold text-black group-hover:text-white">
								Register a new client
							</h3>
							<p class="mt-4 text-base text-gray-600 group-hover:text-white">
								Adds a new client to the database without the need to utilise the app. This is
								useful for quick registration of new clients, without the need to install/use the
								app.
							</p>
						</div>
					</a>

					<a
						href="#1"
						class="transition-all duration-1000 bg-white hover:bg-blue-500 hover:shadow-xl m-2 p-4 relative z-40 group rounded-lg"
					>
						<div
							class=" absolute bg-blue-500/50 top-0 left-0 w-24 h-1 z-30 transition-all duration-200 group-hover:bg-white group-hover:w-1/2"
						></div>
						<div class="py-2 px-9 relative">
							<svg
								class="w-16 h-16 fill-gray-400 group-hover:fill-white"
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 32 32"
								id="polo-tshirt"
							>
								<path d="m16.962 5.841 3.582.717-.716-4.115zM12.172 2.443l-.716 4.115 3.582-.717z">
								</path>
								<path
									d="M28.488 7.301a5.354 5.354 0 0 0-2.743-3.305c-.112-.056-2.96-1.2-4.942-1.996l.87 4.987a.52.52 0 0 1-.488.746.535.535 0 0 1-.101-.01L16.5 6.806V12a.5.5 0 1 1-1 0V6.806l-4.583.917a.518.518 0 0 1-.613-.598L11.196 2c-1.982.796-4.828 1.94-4.94 1.996a5.36 5.36 0 0 0-2.75 3.328l-1.492 6.26c-.042.175.01.359.138.486l.608.608a5.487 5.487 0 0 0 3.907 1.618c.196 0 .375-.111.464-.287l1.072-2.145c.013.292.02.584.02.876V28.48c0 .231.153.435.375.499A27.03 27.03 0 0 0 16 30c2.508 0 5.015-.34 7.402-1.022a.52.52 0 0 0 .376-.5V14.74c0-.292.006-.584.019-.876l1.073 2.145a.519.519 0 0 0 .463.287 5.487 5.487 0 0 0 3.907-1.618l.608-.608a.518.518 0 0 0 .138-.487l-1.498-6.282zM17.03 11.5c-.276 0-.505-.224-.505-.5s.219-.5.495-.5h.01a.5.5 0 0 1 0 1zm0-2c-.276 0-.505-.224-.505-.5s.219-.5.495-.5h.01a.5.5 0 0 1 0 1z"
								>
								</path>
							</svg>

							<h3 class="mt-8 text-lg font-semibold text-black group-hover:text-white">
								Registered Clients
							</h3>
							<p class="mt-4 text-base text-gray-600 group-hover:text-white">
								View all registered clients, alongside their uploaded documents.
							</p>
						</div>
					</a>

					<a
						href="#1"
						class="transition-all duration-1000 bg-white hover:bg-blue-500 hover:shadow-xl m-2 p-4 relative z-40 group rounded-lg"
					>
						<div
							class=" absolute bg-blue-500/50 top-0 left-0 w-24 h-1 z-30 transition-all duration-200 group-hover:bg-white group-hover:w-1/2"
						></div>
						<div class="py-2 px-9 relative">
							<svg
								class="w-10 h-10 mb-3 text-gray-400 group-hover:text-white "
								fill="none"
								stroke="currentColor "
								viewBox="0 0 24 24"
								xmlns="http://www.w3.org/2000/svg"
								><path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
								></path></svg
							>

							<h3 class="mt-8 text-lg font-semibold text-black group-hover:text-white">
								Upload PDF
							</h3>
							<p class="mt-4 text-base text-gray-600 group-hover:text-white">
								Quickly Upload PDF invoices or receipts.
							</p>
						</div>
					</a><a
						href="#1"
						class="transition-all duration-1000 bg-white hover:bg-blue-500 hover:shadow-xl m-2 p-4 relative z-40 group rounded-lg"
					>
						<div
							class=" absolute bg-blue-500/50 top-0 left-0 w-24 h-1 z-30 transition-all duration-200 group-hover:bg-white group-hover:w-1/2"
						></div>
						<div class="py-2 px-9 relative">
							<span class="text-gray-400 opacity-75 group-hover:text-white">
								<svg
									class="w-14 h-14"
									xmlns="http://www.w3.org/2000/svg"
									fill="none"
									viewBox="0 0 24 24"
									stroke-width="1.5"
									stroke="currentColor"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"
									/>
								</svg>
							</span>

							<h3 class="mt-8 text-lg font-semibold text-black group-hover:text-white">
								Upload Photos
							</h3>
							<p class="mt-4 text-base text-gray-600 group-hover:text-white">
								Quickly Upload photos of invoices or receipts.
							</p>
						</div>
					</a>
				</div>
			</div>
		</div>
	</div>
</div>
