import React from "react";
import { StyleSheet, Text, View } from "react-native";

export default function Toast({ toast }) {
  if (!toast) return null;
  return (
    <View style={[styles.toast, toast.tone === "error" && styles.error, toast.tone === "success" && styles.success]}>
      <Text style={styles.text}>{toast.message}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  toast: {
    position: "absolute",
    top: 58,
    left: 18,
    right: 18,
    zIndex: 30,
    borderLeftWidth: 4,
    borderLeftColor: "#2454e6",
    borderRadius: 16,
    backgroundColor: "#ffffff",
    padding: 14,
    shadowColor: "#1e2c53",
    shadowOpacity: 0.16,
    shadowRadius: 24,
    elevation: 8,
  },
  error: { borderLeftColor: "#e5324f" },
  success: { borderLeftColor: "#0f9f6e" },
  text: { color: "#151a2d", fontWeight: "700" },
});

