const width = window.innerWidth;
const height = window.innerHeight;

const projection = d3.geoOrthographic()
    .scale(window.innerHeight * 0.45)
    .translate([width / 2, height / 2])
    .rotate([0, -90]) // Center on North Pole
    .clipAngle(90);

const path = d3.geoPath().projection(projection);

const svg = d3.select("#map")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

// Background globe circle
svg.append("circle")
    .attr("cx", width / 2)
    .attr("cy", height / 2)
    .attr("r", projection.scale())
    .attr("class", "water");

const g = svg.append("g");

// Graticule
const graticule = d3.geoGraticule();
g.append("path")
    .datum(graticule)
    .attr("class", "graticule")
    .attr("d", path);

const routesData = {
    nsr: {
        title: "东北航道 (Northern Sea Route)",
        description: "由鹿特丹出发，经挪威北角、巴伦支海、喀拉海、拉普捷夫海、东西伯利亚海，穿过白令海峡到达横滨。它是目前开发程度最高、商业利用价值最大的北极航道。通过此航道，从大连前往鹿特丹可比传统经苏伊士运河缩短航程约2740海里。",
        details: [
            "夏季航行窗口：7月至11月",
            "主要货类：液化天然气(LNG)、原油、铁矿石",
            "战略意义：俄罗斯北极战略的核心，中国'冰上丝绸之路'的重点",
            "风险：极区浮冰、低温环境对船体材料要求高"
        ],
        color: "#00d2ff",
        coords: [
            [4.4, 51.9],     // Rotterdam
            [23.6, 70.6],    // Hammerfest
            [58.0, 70.5],    // Kara Strait
            [73, 73],        // Yamal (Sabetta)
            [100, 78],       // Severnaya Zemlya
            [140, 76],       // Laptev Sea
            [160, 72],       // East Siberian Sea
            [170, 68],       // Pevek
            [-170, 66],      // Bering Strait
            [139.7, 35.4]    // Yokohama
        ],
        distance: "约 13,000 km",
        time: "18-22 天",
        saving: "缩短 35-40%"
    },
    nwp: {
        title: "西北航道 (Northwest Passage)",
        description: "连接大西洋和太平洋，穿过加拿大北极群岛。虽然目前受多年冰影响较大，通航难度高于东北航道，但它是连接美洲东西海岸或美亚之间的潜在黄金水道。",
        details: [
            "主要经由：戴维斯海峡、博福特海",
            "环境：冰山风险较高，岛礁众多，水道复杂",
            "主权状态：加拿大主张为内水，存在国际争议",
            "生态：途经多个极地野生动物保护区"
        ],
        color: "#f39c12",
        coords: [
            [4.4, 51.9],      // Rotterdam
            [-50, 60],        // South of Greenland
            [-65, 65],        // Davis Strait
            [-80, 74.2],      // Lancaster Sound
            [-100, 74.5],     // Parry Channel
            [-125, 71.9],     // Amundsen Gulf
            [-150, 71],       // Beaufort Sea
            [-170, 66],       // Bering Strait
            [139.7, 35.4]     // Yokohama
        ],
        distance: "约 14,000 km",
        time: "20-25 天",
        saving: "缩短 25-30%"
    },
    tsr: {
        title: "穿极航道 (Transpolar Sea Route)",
        description: "直接穿越北极点的航道。这是理论上欧亚之间最短的路径，完全处于公海水域，避开了沿岸国的管辖权争议。随着全球变暖北极冰盖消退，其未来潜力巨大。",
        details: [
            "地理优势：不经过浅滩海峡，适合超大型油轮（ULCC）",
            "通航条件：预计2035-2045年开始具备季节性商业通航可能",
            "管理：受国际海事组织(IMO)极地规则(Polar Code)监管",
            "深度：水深充足，无通过吃水限制"
        ],
        color: "#9b59b6",
        coords: [
            [4.4, 51.9],
            [10, 75],
            [18, 80],
            [0, 90],         // North Pole
            [170, 80],
            [170, 70],
            [-170, 66],
            [139.7, 35.4]
        ],
        distance: "约 11,500 km",
        time: "14-18 天",
        saving: "缩短 50%+"
    },
    suez: {
        title: "传统航道 (Suez Canal Route)",
        description: "由于传统欧亚贸易。尽管北极航道在缩短距离上有优势，但苏伊士航道目前仍是全年稳定通航的支柱，支持着全球超过12%的贸易量。",
        details: [
            "限制：苏伊士运河通过费昂贵，海盗风险（曼德海峡）",
            "天气：常年受季风影响，但在温带和热带区域运行",
            "状态：运河扩建后可通行大部分巨轮",
            "核心节点：直布罗陀、苏伊士、马六甲"
        ],
        color: "#e74c3c",
        coords: [
            [4.4, 51.9],
            [-10, 45],       // Cape Finisterre
            [-5, 36],        // Strait of Gibraltar
            [32.5, 30.5],    // Port Said (Suez Canal)
            [42, 12],        // Bab el-Mandeb
            [80, 6],         // Sri Lanka
            [101.5, 2.5],    // Strait of Malacca
            [121, 24],       // Taiwan Strait
            [139.7, 35.4]
        ],
        distance: "约 21,500 km",
        time: "35-42 天",
        saving: "基准 (0%)"
    }
};

const cities = [
    { name: "鹿特丹 / Rotterdam", coords: [4.4, 51.9] },
    { name: "横滨 / Yokohama", coords: [139.7, 35.4] }
];

async function init() {
    try {
        const world = await d3.json("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json");
        const countries = topojson.feature(world, world.objects.countries);

        g.append("path")
            .datum(countries)
            .attr("class", "land")
            .attr("d", path);

        // Add pole indicator
        g.append("circle")
            .attr("cx", projection([0, 90])[0])
            .attr("cy", projection([0, 90])[1])
            .attr("r", 4)
            .attr("fill", "#4fc3f7")
            .attr("class", "pole");

        // Add cities
        g.selectAll(".city-dot")
            .data(cities)
            .enter()
            .append("circle")
            .attr("cx", d => projection(d.coords)[0])
            .attr("cy", d => projection(d.coords)[1])
            .attr("r", 5)
            .attr("fill", "#fff")
            .style("filter", "drop-shadow(0 0 5px #fff)");

        g.selectAll(".city-label")
            .data(cities)
            .enter()
            .append("text")
            .attr("class", "city-label")
            .attr("x", d => projection(d.coords)[0] + 10)
            .attr("y", d => projection(d.coords)[1] + 5)
            .text(d => d.name);

        // Draw routes function
        window.drawRoute = function (id) {
            // Remove existing if any
            removeRoute(id);

            const data = routesData[id];
            const routeG = g.append("g").attr("class", `route-group route-${id}`);

            const pathElement = routeG.append("path")
                .datum(data.coords)
                .attr("class", "route-path")
                .attr("d", getLineGenerator())
                .style("stroke", data.color)
                .style("opacity", 0);

            pathElement.transition()
                .duration(1000)
                .style("opacity", 1);

            // Ship animation
            const ship = routeG.append("circle")
                .attr("class", "ship")
                .attr("r", 5)
                .attr("fill", data.color)
                .style("opacity", 0);

            animateShip(ship, data);
        };

        function getLineGenerator() {
            return d3.line()
                .x(d => projection(d)[0])
                .y(d => projection(d)[1])
                .curve(d3.curveCatmullRom.alpha(0.5));
        }

        function animateShip(ship, data) {
            ship.style("opacity", 1);
            const points = data.coords;
            let currentSegment = 0;

            function moveToNext() {
                const start = points[currentSegment];
                const end = points[(currentSegment + 1) % points.length];
                const interpolate = d3.geoInterpolate(start, end);

                ship.transition()
                    .duration(3000)
                    .ease(d3.easeLinear)
                    .attrTween("transform", function () {
                        return function (t) {
                            const coords = interpolate(t);
                            const p = projection(coords);
                            ship.attr("data-coords", JSON.stringify(coords));
                            // Handle visibility
                            const visible = isVisible(coords);
                            ship.style("opacity", visible ? 1 : 0);
                            return `translate(${p[0]},${p[1]})`;
                        };
                    })
                    .on("end", () => {
                        currentSegment = (currentSegment + 1) % (points.length - 1);
                        if (currentSegment === 0) {
                            // Loop back to start
                            moveToNext();
                        } else {
                            moveToNext();
                        }
                    });
            }
            moveToNext();
        }

        window.removeRoute = function (id) {
            d3.selectAll(`.route-${id}`).remove();
        };

        // Initial route
        drawRoute('nsr');

        // Event Listeners
        d3.selectAll('input[type="checkbox"]').on("change", function () {
            const id = d3.select(this).attr("data-route");
            if (this.checked) {
                drawRoute(id);
                updateInfo(id);
            } else {
                removeRoute(id);
            }
        });

        function updateInfo(id) {
            const data = routesData[id];
            d3.select("#route-title").text(data.title);
            d3.select("#route-description").text(data.description);
            d3.select("#distance-stat .value").text(data.distance);
            d3.select("#time-stat .value").text(data.time);
            d3.select("#saving-stat .value").text(data.saving);

            // Render details list
            const detailsList = d3.select("#route-details");
            detailsList.html("");
            data.details.forEach(detail => {
                detailsList.append("li").text(detail);
            });

            // Highlight info panel
            d3.select("#info-panel").style("box-shadow", `0 8px 32px ${data.color}44`);
        }

        // Zoom and Pan (Rotation)
        const drag = d3.drag().on("drag", (event) => {
            const rotate = projection.rotate();
            const k = 0.2; // sensitivity
            projection.rotate([
                rotate[0] + event.dx * k,
                rotate[1] - event.dy * k
            ]);
            updateMap();
        });

        svg.call(drag);

        function updateMap() {
            g.selectAll("path.land").attr("d", path);
            g.selectAll("path.graticule").attr("d", path);

            g.selectAll(".city-dot")
                .attr("cx", d => projection(d.coords)[0])
                .attr("cy", d => projection(d.coords)[1])
                .style("opacity", d => isVisible(d.coords) ? 1 : 0);

            g.selectAll(".city-label")
                .attr("x", d => projection(d.coords)[0] + 10)
                .attr("y", d => projection(d.coords)[1] + 5)
                .style("opacity", d => isVisible(d.coords) ? 1 : 0);

            g.selectAll(".route-path").attr("d", getLineGenerator());

            // Update ship positions during drag
            g.selectAll(".ship").each(function () {
                const ship = d3.select(this);
                const coordsStr = ship.attr("data-coords");
                if (coordsStr) {
                    const coords = JSON.parse(coordsStr);
                    const p = projection(coords);
                    ship.attr("transform", `translate(${p[0]},${p[1]})`);
                    ship.style("opacity", isVisible(coords) ? 1 : 0);
                }
            });

            // Pole indicator
            g.select(".pole")
                .attr("cx", projection([0, 90])[0])
                .attr("cy", projection([0, 90])[1])
                .style("opacity", isVisible([0, 90]) ? 1 : 0);
        }

        function isVisible(coords) {
            // Check if point is on visible hemisphere
            const r = projection.rotate();
            const p = d3.geoDistance(coords, [-r[0], -r[1]]);
            return p < Math.PI / 2;
        }

        // Handle window resize
        window.addEventListener("resize", () => {
            const newWidth = window.innerWidth;
            const newHeight = window.innerHeight;
            svg.attr("width", newWidth).attr("height", newHeight);
            projection.translate([newWidth / 2, newHeight / 2]);
            updateMap();
        });

    } catch (error) {
        console.error("Error loading map data:", error);
    }
}

init();
