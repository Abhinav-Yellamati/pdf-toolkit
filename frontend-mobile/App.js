import React, { useEffect, useMemo, useRef, useState } from "react";
import { ActivityIndicator, Animated, Pressable, ScrollView, StyleSheet, Text, TextInput, View } from "react-native";
import { SafeAreaProvider, SafeAreaView } from "react-native-safe-area-context";
import * as DocumentPicker from "expo-document-picker";
import { StatusBar } from "expo-status-bar";
import { Ionicons } from "@expo/vector-icons";
import ErrorBoundary from "./src/components/ErrorBoundary";
import Toast from "./src/components/Toast";
import ToolCard from "./src/components/ToolCard";
import UploadBox from "./src/components/UploadBox";
import { API_BASE } from "./src/config/api";
import { initialFields, tools } from "./src/config/tools";
import { checkApiHealth, runTool, shareDownload } from "./src/services/api";
import { logError, logInfo } from "./src/utils/logger";
import { validateFields, validateFiles } from "./src/utils/validation";

function AppContent() {
  const [activeId, setActiveId] = useState("compress");
  const [files, setFiles] = useState([]);
  const [fields, setFields] = useState(initialFields(tools[0]));
  const [progress, setProgress] = useState(0);
  const [isWorking, setIsWorking] = useState(false);
  const [download, setDownload] = useState(null);
  const [toast, setToast] = useState(null);
  const activeTool = useMemo(() => tools.find((tool) => tool.id === activeId) || tools[0], [activeId]);
  const fade = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    logInfo("startup", "Mobile app mounted", {
      apiBase: API_BASE,
      toolCount: tools.length,
      initialTool: activeTool.id,
    });

    checkApiHealth().catch((error) => {
      logError("startup", "Backend health check failed during startup", error);
    });
  }, []);

  useEffect(() => {
    fade.setValue(0);
    Animated.timing(fade, {
      toValue: 1,
      duration: 220,
      useNativeDriver: true,
    }).start();
  }, [activeId, fade]);

  function showToast(message, tone = "info") {
    setToast({ message, tone });
    setTimeout(() => setToast(null), 3200);
  }

  function selectTool(tool) {
    setActiveId(tool.id);
    setFiles([]);
    setFields(initialFields(tool));
    setProgress(0);
    setDownload(null);
  }

  async function pickFiles() {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        multiple: activeTool.multiple,
        type: activeTool.mimeTypes,
        copyToCacheDirectory: true,
      });
      if (result.canceled) return;
      const selected = result.assets || [];
      const error = validateFiles(activeTool, selected);
      if (error) {
        showToast(error, "error");
        return;
      }
      logInfo("upload", "Files selected", {
        tool: activeTool.id,
        count: selected.length,
        names: selected.map((file) => file.name),
      });
      setFiles(selected);
      setDownload(null);
      showToast(`${selected.length} file${selected.length > 1 ? "s" : ""} ready.`);
    } catch (error) {
      logError("upload", "Document picker failed", error);
      showToast("Could not open the file picker. Please try again.", "error");
    }
  }

  async function runActiveTool() {
    const fileError = validateFiles(activeTool, files);
    if (fileError) {
      showToast(fileError, "error");
      return;
    }
    const fieldError = validateFields(activeTool, fields);
    if (fieldError) {
      showToast(fieldError, "error");
      return;
    }

    setIsWorking(true);
    setProgress(8);
    setDownload(null);
    try {
      const result = await runTool(activeTool, files, fields, setProgress);
      setDownload(result);
      showToast(`${activeTool.title} completed.`, "success");
    } catch (error) {
      logError("runtime", `Tool execution failed for ${activeTool.id}`, error);
      setProgress(0);
      showToast(error.message || "Processing failed.", "error");
    } finally {
      setIsWorking(false);
    }
  }

  async function shareResult() {
    try {
      await shareDownload(download);
    } catch (error) {
      logError("share", "Share failed", error);
      showToast(error.message, "error");
    }
  }

  return (
    <SafeAreaProvider>
      <SafeAreaView style={styles.safe} edges={["top", "left", "right"]}>
        <StatusBar style="dark" />
        <Toast toast={toast} />
        <View style={styles.header}>
          <View style={styles.brandMark}>
            <Ionicons name="document-text-outline" size={24} color="#ffffff" />
          </View>
          <View style={styles.brandCopy}>
            <Text style={styles.brand}>PDF Toolkit</Text>
            <Text style={styles.brandSub}>Mobile document studio</Text>
          </View>
        </View>

        <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
          <View style={styles.hero}>
            <Text style={styles.eyebrow}>Production PDF suite</Text>
            <Text style={styles.title}>Powerful PDF tools for mobile workflows.</Text>
            <Text style={styles.subtitle}>Upload, process, download and share files using the same FastAPI backend as the web app.</Text>
          </View>

          <Animated.View style={[styles.workspace, { opacity: fade, transform: [{ translateY: fade.interpolate({ inputRange: [0, 1], outputRange: [10, 0] }) }] }]}>
            <View style={styles.workspaceHead}>
              <View style={styles.toolBadge}>
                <Ionicons name={activeTool.icon} size={24} color="#ffffff" />
              </View>
              <View style={styles.workspaceCopy}>
                <Text style={styles.workspaceTitle}>{activeTool.title}</Text>
                <Text style={styles.workspaceText}>{activeTool.description}</Text>
              </View>
            </View>

            <UploadBox files={files} multiple={activeTool.multiple} onPick={pickFiles} onClear={() => setFiles([])} />

            {(activeTool.fields || []).map((field) => (
              <View style={styles.field} key={field.name}>
                <Text style={styles.fieldLabel}>{field.label}</Text>
                <TextInput
                  secureTextEntry={field.secure}
                  keyboardType={field.type === "number" ? "numeric" : "default"}
                  placeholder={field.placeholder}
                  value={fields[field.name]}
                  onChangeText={(value) => setFields((current) => ({ ...current, [field.name]: value }))}
                  style={styles.input}
                  placeholderTextColor="#94a3b8"
                />
              </View>
            ))}

            <View style={styles.progressTrack}>
              <View style={[styles.progressFill, { width: `${progress}%` }]} />
            </View>
            {isWorking && <Text style={styles.processingHint}>Optimizing file on the FastAPI backend...</Text>}

            <Pressable style={[styles.primaryButton, isWorking && styles.disabled]} onPress={runActiveTool} disabled={isWorking}>
              {isWorking ? <ActivityIndicator color="#ffffff" /> : <Ionicons name="cloud-upload-outline" size={20} color="#ffffff" />}
              <Text style={styles.primaryText}>{isWorking ? "Processing..." : `Run ${activeTool.title}`}</Text>
            </Pressable>

            {download && (
              <View style={styles.downloadCard}>
                <Text style={styles.ready}>Ready</Text>
                <Text style={styles.downloadName}>{download.filename}</Text>
                <Pressable style={styles.shareButton} onPress={shareResult}>
                  <Ionicons name="share-outline" size={18} color="#ffffff" />
                  <Text style={styles.shareText}>Share or save</Text>
                </Pressable>
              </View>
            )}
          </Animated.View>

          <View style={styles.sectionHead}>
            <Text style={styles.sectionKicker}>Dashboard</Text>
            <Text style={styles.sectionTitle}>All PDF tools</Text>
          </View>
          <View style={styles.grid}>
            {tools.map((tool) => (
              <ToolCard key={tool.id} tool={tool} active={tool.id === activeId} onPress={() => selectTool(tool)} />
            ))}
          </View>
        </ScrollView>

        <View style={styles.bottomNav}>
          {[
            ["compress", "flash-outline", "Compress"],
            ["merge", "git-merge-outline", "Merge"],
            ["split", "cut-outline", "Split"],
            ["protect", "lock-closed-outline", "Secure"],
          ].map(([id, icon, label]) => (
            <Pressable key={id} style={styles.navItem} onPress={() => selectTool(tools.find((tool) => tool.id === id))}>
              <Ionicons name={icon} size={22} color={activeId === id ? "#e5324f" : "#657086"} />
              <Text style={[styles.navText, activeId === id && styles.navTextActive]}>{label}</Text>
            </Pressable>
          ))}
        </View>
      </SafeAreaView>
    </SafeAreaProvider>
  );
}

export default function App() {
  return (
    <ErrorBoundary>
      <AppContent />
    </ErrorBoundary>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: "#f6f8fc" },
  header: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 18,
    paddingVertical: 14,
    borderBottomWidth: 1,
    borderBottomColor: "#dde5f2",
    backgroundColor: "#ffffff",
  },
  brandCopy: { flex: 1, marginLeft: 12 },
  brandMark: {
    width: 46,
    height: 46,
    borderRadius: 16,
    backgroundColor: "#e5324f",
    alignItems: "center",
    justifyContent: "center",
  },
  brand: { color: "#151a2d", fontSize: 20, fontWeight: "900" },
  brandSub: { color: "#657086", marginTop: 2 },
  content: { padding: 18, paddingBottom: 104 },
  hero: {
    marginBottom: 18,
    padding: 16,
    borderRadius: 24,
    backgroundColor: "#ffffff",
    borderWidth: 1,
    borderColor: "#dde5f2",
  },
  eyebrow: { color: "#e5324f", fontWeight: "900", marginBottom: 8 },
  title: { color: "#151a2d", fontSize: 34, lineHeight: 38, fontWeight: "900" },
  subtitle: { color: "#657086", fontSize: 16, lineHeight: 24, marginTop: 10 },
  workspace: {
    borderWidth: 1,
    borderColor: "#dde5f2",
    borderRadius: 26,
    backgroundColor: "#ffffff",
    padding: 16,
    shadowColor: "#1e2c53",
    shadowOpacity: 0.14,
    shadowRadius: 28,
    elevation: 6,
  },
  workspaceHead: { flexDirection: "row", marginBottom: 14 },
  toolBadge: {
    width: 54,
    height: 54,
    borderRadius: 18,
    backgroundColor: "#2454e6",
    alignItems: "center",
    justifyContent: "center",
  },
  workspaceCopy: { flex: 1, marginLeft: 12 },
  workspaceTitle: { color: "#151a2d", fontSize: 22, fontWeight: "900" },
  workspaceText: { color: "#657086", lineHeight: 20, marginTop: 3 },
  field: { marginTop: 12 },
  fieldLabel: { color: "#657086", fontWeight: "800", marginBottom: 6 },
  input: {
    minHeight: 48,
    borderWidth: 1,
    borderColor: "#dde5f2",
    borderRadius: 14,
    color: "#151a2d",
    backgroundColor: "#ffffff",
    paddingHorizontal: 12,
  },
  progressTrack: { height: 9, borderRadius: 99, overflow: "hidden", backgroundColor: "#eef4ff", marginVertical: 14 },
  progressFill: { height: "100%", borderRadius: 99, backgroundColor: "#e5324f" },
  processingHint: { color: "#657086", fontWeight: "700", marginBottom: 12, textAlign: "center" },
  primaryButton: {
    minHeight: 52,
    borderRadius: 16,
    backgroundColor: "#e5324f",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
  },
  disabled: { opacity: 0.7 },
  primaryText: { color: "#ffffff", fontWeight: "900", fontSize: 16, marginLeft: 8 },
  downloadCard: {
    marginTop: 14,
    borderWidth: 1,
    borderColor: "#9de5ca",
    borderRadius: 18,
    backgroundColor: "#effcf7",
    padding: 14,
  },
  ready: { color: "#0f9f6e", fontWeight: "900" },
  downloadName: { color: "#151a2d", fontWeight: "900", fontSize: 16, marginVertical: 8 },
  shareButton: {
    alignSelf: "flex-start",
    borderRadius: 14,
    backgroundColor: "#0f9f6e",
    paddingHorizontal: 14,
    paddingVertical: 10,
    flexDirection: "row",
    alignItems: "center",
  },
  shareText: { color: "#ffffff", fontWeight: "900", marginLeft: 6 },
  sectionHead: { marginTop: 24, marginBottom: 12 },
  sectionKicker: { color: "#e5324f", fontWeight: "900" },
  sectionTitle: { color: "#151a2d", fontSize: 26, fontWeight: "900" },
  grid: { flexDirection: "row", flexWrap: "wrap", justifyContent: "space-between" },
  bottomNav: {
    position: "absolute",
    left: 14,
    right: 14,
    bottom: 14,
    borderWidth: 1,
    borderColor: "#dde5f2",
    borderRadius: 24,
    backgroundColor: "#ffffff",
    flexDirection: "row",
    justifyContent: "space-around",
    paddingVertical: 10,
    shadowColor: "#1e2c53",
    shadowOpacity: 0.16,
    shadowRadius: 24,
    elevation: 8,
  },
  navItem: { alignItems: "center", minWidth: 62 },
  navText: { color: "#657086", fontSize: 11, fontWeight: "800", marginTop: 3 },
  navTextActive: { color: "#e5324f" },
});
