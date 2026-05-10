import React from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";
import { Ionicons } from "@expo/vector-icons";

export default function ToolCard({ tool, active, onPress }) {
  return (
    <Pressable style={[styles.card, active && styles.active]} onPress={onPress}>
      <View style={styles.icon}>
        <Ionicons name={tool.icon} size={22} color="#ffffff" />
      </View>
      <Text style={styles.title}>{tool.title}</Text>
      <Text style={styles.description}>{tool.description}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  card: {
    width: "48%",
    minHeight: 154,
    borderWidth: 1,
    borderColor: "#dde5f2",
    borderRadius: 20,
    backgroundColor: "#ffffff",
    padding: 14,
    marginBottom: 12,
    shadowColor: "#1f2a44",
    shadowOpacity: 0.08,
    shadowRadius: 18,
    elevation: 3,
    transform: [{ scale: 1 }],
  },
  active: {
    borderColor: "#e5324f",
    transform: [{ translateY: -2 }],
    backgroundColor: "#fff7f8",
  },
  icon: {
    width: 44,
    height: 44,
    borderRadius: 14,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#e5324f",
    marginBottom: 12,
  },
  title: {
    color: "#151a2d",
    fontSize: 16,
    fontWeight: "800",
    marginBottom: 6,
  },
  description: {
    color: "#657086",
    lineHeight: 18,
    fontSize: 12,
  },
});
