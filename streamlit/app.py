import tensorflow as tf
import streamlit as st
from streamlit_elements import elements, mui, html
from streamlit_elements import media
import streamlit_elements as elem

# Create a sidebar with navigation links
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Page 1", "Page 2"])

# Use the page variable to determine which page to display
if page == "Page 1":
    st.title("Camera")

    img_file_buffer = st.camera_input("Take a picture")

    if img_file_buffer is not None:
        # To read image file buffer as a 3D uint8 tensor with TensorFlow:
        bytes_data = img_file_buffer.getvalue()
        img_tensor = tf.io.decode_image(bytes_data, channels=3)

        # Check the type of img_tensor:
        # Should output: <class 'tensorflow.python.framework.ops.EagerTensor'>
        st.write(type(img_tensor))

        # Check the shape of img_tensor:
        # Should output shape: (height, width, channels)
        st.write(img_tensor.shape)

if page == "Page 2":
    st.title("Tracker")
    # First, import the elements you need
    # Create a frame where Elements widgets will be displayed.
    #
    # Elements widgets will not render outside of this frame.
    # Native Streamlit widgets will not render inside this frame.
    #
    # elements() takes a key as parameter.
    # This key can't be reused by another frame or Streamlit widget.

with elements("dashboard"):

    # You can create a draggable and resizable dashboard using
    # any element available in Streamlit Elements.

    from streamlit_elements import dashboard

    # First, build a default layout for every element you want to include in your dashboard

    layout = [
        # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
        dashboard.Item("first_item", 0, 0, 2, 2),
        dashboard.Item("second_item", 2, 0, 2, 2, isDraggable=False, moved=False),
        dashboard.Item("third_item", 0, 2, 1, 1, isResizable=False),
    ]


    # If you want to retrieve updated layout values as the user move or resize dashboard items,
    # you can pass a callback to the onLayoutChange event parameter.

    def handle_layout_change(updated_layout):
        # You can save the layout in a file, or do anything you want with it.
        # You can pass it back to dashboard.Grid() if you want to restore a saved layout.
        print(updated_layout)

    with dashboard.Grid(layout, onLayoutChange=handle_layout_change):
        with elements("nivo_charts"):

        # Streamlit Elements includes 45 dataviz components powered by Nivo.

            from streamlit_elements import nivo

            DATA = [
                { "taste": "fruity", "chardonay": 93, "carmenere": 61, "syrah": 114 },
                { "taste": "bitter", "chardonay": 91, "carmenere": 37, "syrah": 72 },
                { "taste": "heavy", "chardonay": 56, "carmenere": 95, "syrah": 99 },
                { "taste": "strong", "chardonay": 64, "carmenere": 90, "syrah": 30 },
                { "taste": "sunny", "chardonay": 119, "carmenere": 94, "syrah": 103 },
            ]

            with mui.Box(sx={"bgcolor": "background.paper","boxShadow": 1,"borderRadius": 2,"p": 2,"minWidth": 300,}, key="first_item"):
                nivo.Radar(
                    data=DATA,
                    keys=[ "chardonay", "carmenere", "syrah" ],
                    indexBy="taste",
                    valueFormat=">-.2f",
                    margin={ "top": 70, "right": 80, "bottom": 40, "left": 80 },
                    borderColor={ "from": "color" },
                    gridLabelOffset=36,
                    dotSize=10,
                    dotColor={ "theme": "background" },
                    dotBorderWidth=2,
                    motionConfig="wobbly",
                    legends=[
                        {
                            "anchor": "top-left",
                            "direction": "column",
                            "translateX": -50,
                            "translateY": -40,
                            "itemWidth": 80,
                            "itemHeight": 20,
                            "itemTextColor": "#999",
                            "symbolSize": 12,
                            "symbolShape": "circle",
                            "effects": [
                                {
                                    "on": "hover",
                                    "style": {
                                        "itemTextColor": "#000"
                                    }
                                }
                            ]
                        }
                    ],
                    theme={
                        "background": "#FFFFFF",
                        "textColor": "#31333F",
                        "tooltip": {
                            "container": {
                                "background": "#FFFFFF",
                                "color": "#31333F",
                            }
                        }
                    }
                )
        html.div(
        "This has a hotpink background",
        css={
            "backgroundColor": "hotpink",
            "&:hover": {
                "color": "lightgreen"
            }
        }
    )

        with mui.Box(sx={"flex": 1, "minHeight": 0}):
                        nivo.Pie(
                            data=DATA,
                            theme=self._theme["dark" if self._dark_mode else "light"],
                            margin={ "top": 40, "right": 80, "bottom": 80, "left": 80 },
                            innerRadius=0.5,
                            padAngle=0.7,
                            cornerRadius=3,
                            activeOuterRadiusOffset=8,
                            borderWidth=1,
                            borderColor={
                                "from": "color",
                                "modifiers": [
                                    [
                                        "darker",
                                        0.2,
                                    ]
                                ]
                            },
                            arcLinkLabelsSkipAngle=10,
                            arcLinkLabelsTextColor="grey",
                            arcLinkLabelsThickness=2,
                            arcLinkLabelsColor={ "from": "color" },
                            arcLabelsSkipAngle=10,
                            arcLabelsTextColor={
                                "from": "color",
                                "modifiers": [
                                    [
                                        "darker",
                                        2
                                    ]
                                ]
                            },
                            defs=[
                                {
                                    "id": "dots",
                                    "type": "patternDots",
                                    "background": "inherit",
                                    "color": "rgba(255, 255, 255, 0.3)",
                                    "size": 4,
                                    "padding": 1,
                                    "stagger": True
                                },
                                {
                                    "id": "lines",
                                    "type": "patternLines",
                                    "background": "inherit",
                                    "color": "rgba(255, 255, 255, 0.3)",
                                    "rotation": -45,
                                    "lineWidth": 6,
                                    "spacing": 10
                                }
                            ],
                            fill=[
                                { "match": { "id": "ruby" }, "id": "dots" },
                                { "match": { "id": "c" }, "id": "dots" },
                                { "match": { "id": "go" }, "id": "dots" },
                                { "match": { "id": "python" }, "id": "dots" },
                                { "match": { "id": "scala" }, "id": "lines" },
                                { "match": { "id": "lisp" }, "id": "lines" },
                                { "match": { "id": "elixir" }, "id": "lines" },
                                { "match": { "id": "javascript" }, "id": "lines" }
                            ],
                            legends=[
                                {
                                    "anchor": "bottom",
                                    "direction": "row",
                                    "justify": False,
                                    "translateX": 0,
                                    "translateY": 56,
                                    "itemsSpacing": 0,
                                    "itemWidth": 100,
                                    "itemHeight": 18,
                                    "itemTextColor": "#999",
                                    "itemDirection": "left-to-right",
                                    "itemOpacity": 1,
                                    "symbolSize": 18,
                                    "symbolShape": "circle",
                                    "effects": [
                                        {
                                            "on": "hover",
                                            "style": {
                                                "itemTextColor": "#000"
                                            }
                                        }
                                    ]
                                }
                            ]
                        )
        mui.Paper("Third item (cannot resize)", key="third_item")
