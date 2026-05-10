import React from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";
import { logError } from "../utils/logger";

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { error: null };
  }

  static getDerivedStateFromError(error) {
    return { error };
  }

  componentDidCatch(error, info) {
    logError("runtime", "Unhandled render error", error);
    console.error("[PDFToolkit:runtime] Component stack", info?.componentStack);
  }

  render() {
    if (!this.state.error) {
      return this.props.children;
    }

    return (
      <View style={styles.screen}>
        <View style={styles.card}>
          <Text style={styles.kicker}>Runtime error</Text>
          <Text style={styles.title}>PDF Toolkit could not render this screen.</Text>
          <Text style={styles.message}>{this.state.error.message || "Unknown error"}</Text>
          <Pressable style={styles.button} onPress={() => this.setState({ error: null })}>
            <Text style={styles.buttonText}>Try again</Text>
          </Pressable>
        </View>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#f6f8fc",
    padding: 20,
  },
  card: {
    width: "100%",
    borderWidth: 1,
    borderColor: "#dde5f2",
    borderRadius: 20,
    backgroundColor: "#ffffff",
    padding: 18,
  },
  kicker: { color: "#e5324f", fontWeight: "900", marginBottom: 8 },
  title: { color: "#151a2d", fontSize: 20, fontWeight: "900", marginBottom: 8 },
  message: { color: "#657086", lineHeight: 20 },
  button: {
    alignSelf: "flex-start",
    marginTop: 14,
    borderRadius: 14,
    backgroundColor: "#e5324f",
    paddingHorizontal: 14,
    paddingVertical: 10,
  },
  buttonText: { color: "#ffffff", fontWeight: "900" },
});
